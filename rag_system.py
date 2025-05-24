# frida_chatbot_project/rag_system.py
import random # Hala kullanılmıyor ama yapıyı koruduk

# --- rag_data.txt dosyasını okuma fonksiyonu ---
def load_document_text(filepath: str) -> str:
    """
    Belirtilen dosya yolundan metni okur. Dosya bulunamazsa veya hata olursa
    boş bir string döndürür ve uyarı mesajı verir.
    """
    try:
        # 'utf-8' encoding is standard and handles Turkish characters
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Uyarı: Belge dosyası bulunamadı: {filepath}. Bilgi geri çekme çalışmayacak.")
        return "" # Dosya yoksa boş metin döndür
    except Exception as e:
        print(f"Hata: Belge dosyası yüklenirken bir sorun oluştu {filepath}: {e}")
        return ""

# --- Belgeyi bölümlere ayırma fonksiyonu ---
def parse_document_sections(text: str) -> dict:
    """
    Metni '## Konu:' başlıklarına göre bölümlere ayırır
    ve bir sözlük olarak döndürür.
    """
    sections = {}
    # Belgeyi '## Konu:' işaretine göre ayır
    parts = text.split('## Konu:')

    # İlk kısım genellikle giriş veya genel bilgidir (başlıksız kısım)
    # Eğer ilk kısım boş değilse bunu 'Giriş/Biyografi' olarak ekle
    if parts[0].strip():
        sections['Biyografi'] = parts[0].strip() # Use 'Biyografi' as a standard key

    # Geri kalan kısımları işle
    for part in parts[1:]:
        # Kısmı başlık satırı ve içerik olarak ayır
        lines = part.strip().split('\n', 1)
        if len(lines) == 2:
            topic = lines[0].strip() # Başlık satırı konu adıdır
            content = lines[1].strip() # Kalan kısım içeriktir
            sections[topic] = content
        elif len(lines) == 1:
            # Sadece başlık var, içerik yok durumu
            topic = lines[0].strip()
            sections[topic] = "" # Konuyu boş içerikle ekle veya logla

    return sections

# --- rag_data.txt dosyasından tüm veriyi yükle ve bölümlere ayır ---
BIOGRAPHICAL_DATA_FILE = 'rag_data.txt'
raw_document_text = load_document_text(BIOGRAPHICAL_DATA_FILE)
# Metni sadece başarıyla yüklendiyse bölümlere ayır
document_sections = {}
if raw_document_text:
    document_sections = parse_document_sections(raw_document_text)

# --- Anahtar kelimeleri bölüm başlıklarına eşleme ---
# Kullanıcının sorgusundaki kelimelerle hangi bölümün ilgili olabileceğini bulmak için
# Bu harita, sorgudaki kelimeler ile parse ettiğimiz bölüm başlıklarını eşler.
KEYWORD_TO_SECTION = {
    "Kimlik": ["kimsin", "kimsiniz", "kendinden bahset", "frida kahlo kimdir", "ben kimim"], # Added "ben kimim"
    "Sanat": ["sanat", "resim", "tablo", "eser", "otoportre", "boyamak", "çizmek"], # Added more art keywords
    "Diego Rivera": ["diego", "rivera", "eş", "evlilik", "kocası", "ilişki"], # Added "ilişki"
    "Acı ve Sağlık": ["acı", "ağrı", "sağlık", "hastalık", "çocuk felci", "felç", "ameliyat"], # Added "ameliyat", removed kaza (now in Biyografi)
    "Meksika Kültürü": ["meksika", "kültür", "elbise", "gelenek", "tehuana", "ülken", "miras"], # Added "miras"
    "Hayat Felsefesi": ["hayat", "felsefe", "yaşam", "düşünce", "viva la vida", "bakış açısı"], # Added "bakış açısı"
    "Biyografi": ["doğum", "doğdu", "nereli", "aile", "baba", "anne", "kaza", "tramvay", "geçmişi", "yaşamı", "biyografi", "hayatı", "çocukluk"] ,# Added "hayatı", "çocukluk"
    "Sevdikleri": ["sevdiğim", "sevdigim", "beğendiklerim", "beğendiğim", "favori", "renk", "kırmızı", "sarı", "örgü", "örmek", "örmeyi"] 

}

# --- Bilgi Geri Çekme (Retrieval) Fonksiyonu ---
def retrieve_relevant_info_tr(query: str) -> str:
    """
    Kullanıcının sorgusuna göre rag_data.txt dosyasındaki ilgili bölümü geri çeker.
    Anahtar kelime eşleştirmesi kullanarak ilgili bölümü bulur.
    Eğer belge yüklenemediyse veya ilgili bölüm bulunamazsa varsayılan mesaj döndürür.
    """
    query_lower = query.lower()

    # Eğer belge hiç yüklenemediyse bilgi ver
    if not document_sections:
         return "Üzgünüm, bilgi kaynaklarıma erişemiyorum."

    # Anahtar kelime eşleştirmesi ile ilgili bölümü bulmaya çalış
    for section_key, keywords in KEYWORD_TO_SECTION.items():
        # Eğer sorgu, bu bölümle ilişkili anahtar kelimelerden herhangi birini içeriyorsa
        if any(keyword in query_lower for keyword in keywords):
            # İlgili bölüm bulunduysa içeriğini döndür
            # document_sections.get() kullanarak bölüm başlığı sözlükte yoksa hata almayı engelle
            return document_sections.get(section_key, f"Üzgünüm, '{section_key}' konusunda bilgi bulamadım.")

    # Eğer hiçbir spesifik anahtar kelime eşleşmezse, genel biyografi bölümünü döndür
    # veya bir "bilgi bulamadım" mesajı ver. Biyografi genellikle iyi bir başlangıç noktasıdır.
    # get() kullanarak 'Biyografi' anahtarı yoksa hata almayı engelle
    return document_sections.get('Biyografi', "Üzgünüm, bu konuda bilgi bulamadım. Başka bir şey sormak ister misin?")

# --- Gerçek RAG sisteminiz için fonksiyonlar buraya gelebilir ---
# Örneğin, belgeleri yükleme, vektör deposu oluşturma, vektör deposunda arama gibi.
# Şu anki retrieve_relevant_info_tr fonksiyonu bu adımları basitçe simüle eder
# ancak artık bilgiyi dış metin dosyasından alıp kullanmaktadır.