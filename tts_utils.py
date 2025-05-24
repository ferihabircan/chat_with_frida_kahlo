# frida_chatbot_project/tts_utils.py
import os
from elevenlabs.client import ElevenLabs
from elevenlabs.types import Voice # Voice sınıfını içe aktardığınızdan emin olun
import tempfile
import uuid
import shutil
import time

import config

TTS_AVAILABLE = config.ELEVEN_LABS_API_KEY_AVAILABLE
ELEVEN_LABS_API_KEY = config.ELEVEN_LABS_API_KEY
TEMP_AUDIO_DIR = config.TEMP_AUDIO_DIR

os.makedirs(TEMP_AUDIO_DIR, exist_ok=True)
print(f"Geçici ses dosyaları klasörü: {TEMP_AUDIO_DIR}")

eleven_labs_client = None
if TTS_AVAILABLE:
    try:
        # Eleven Labs istemcisini başlatın
        # v2+ sürümünde api_key genellikle burada verilir veya ENV değişkeninden alınır
        eleven_labs_client = ElevenLabs(api_key=ELEVEN_LABS_API_KEY)
        print("Eleven Labs istemcisi başarıyla başlatıldı.")
    except Exception as e:
        print(f"HATA: Eleven Labs istemcisi başlatılırken hata oluştu: {e}. Metin-Konuşma devre dışı bırakıldı.")
        eleven_labs_client = None
        TTS_AVAILABLE = False
else:
    print("BİLGİ: Eleven Labs API anahtarı mevcut değil (config'de kontrol edildi), Metin-Konuşma devre dışı.")


# --- Function to Generate and Save Audio ---
def generate_audio_file(text: str) -> str | None:
    """
    Generates audio from text using Eleven Labs (v2.1.0 API) and saves it
    to a temporary file.

    Args:
        text: The text to convert to speech.

    Returns:
        The path to the temporary audio file (str) or None if TTS failed or is disabled.
    """
    if eleven_labs_client is None:
        print("Eleven Labs istemcisi mevcut değil. Ses üretilemiyor.")
        return None

    if not text or not text.strip():
        print("Ses üretimi için metin sağlanmadı.")
        return None

    audio_filepath = None # Define outside try for cleanup
    try:
        # Frida için uygun ses ID'sini kullanın. v2+ convert metodu genellikle doğrudan ID bekler.
        voice_id_to_use = "bqaNYmxFgK1TN7CL95PZ" # Antoinette ID

        print(f"'{text[:50]}...' metni için ses ID'si '{voice_id_to_use}' kullanarak ses üretiliyor...")

        # Use tempfile to create a temporary file
        with tempfile.NamedTemporaryFile(dir=TEMP_AUDIO_DIR, suffix=".mp3", delete=False) as tmp_file:
             audio_filepath = tmp_file.name

             # eleven_labs_client üzerinden text_to_speech modülünü kullanın
             # PARAMETRE ADINI DEĞİŞTİRDİK: 'voice=' yerine 'voice_id=', 'model=' yerine 'model_id='
             audio_stream = eleven_labs_client.text_to_speech.convert(
                text=text,
                voice_id=voice_id_to_use, # İlk düzeltmemiz
                model_id="eleven_multilingual_v2", # BURAYI DEĞİŞTİRDİK: 'model=' yerine 'model_id='
                # stability=0.5, # Bu parametreler 'optimize_streaming_latency' gibi
                # similarity_boost=0.75, # farklı isimler almış olabilir v2+ de, şimdilik yorum satırında kalsın
             )

             # Write the audio stream chunks to the file
             for chunk in audio_stream:
                 if chunk:
                     tmp_file.write(chunk)

        print(f"Ses başarıyla kaydedildi: {audio_filepath}")
        return audio_filepath

    except Exception as e:
        print(f"Eleven Labs TTS üretimi sırasında hata oluştu: {e}")
        if audio_filepath and os.path.exists(audio_filepath):
            try:
                os.remove(audio_filepath)
                print(f"Kısmen oluşturulmuş dosya temizlendi: {audio_filepath}")
            except OSError as cleanup_e:
                print(f"Kısmen oluşturulmuş dosya temizlenirken hata: {cleanup_e}")
        return None

# --- Temizlik Fonksiyonu ---
# (Bu fonksiyonunuz doğru görünüyor, değişiklik yapmaya gerek yok)
def cleanup_old_audio_files(age_seconds: int = 600):
    print(f"'{TEMP_AUDIO_DIR}' dizininde {age_seconds} saniyeden eski dosyalar için temizlik yapılıyor.")
    now = time.time()
    count = 0
    try:
        if not os.path.exists(TEMP_AUDIO_DIR):
            print(f"Temizlik dizini bulunamadı: {TEMP_AUDIO_DIR}")
            return 0

        for filename in os.listdir(TEMP_AUDIO_DIR):
            filepath = os.path.join(TEMP_AUDIO_DIR, filename)
            if os.path.isfile(filepath) and filename.lower().endswith('.mp3'):
                try:
                    mod_time = os.path.getmtime(filepath)
                    if now - mod_time > age_seconds:
                        os.remove(filepath)
                        print(f"Eski dosya kaldırıldı: {filepath}")
                        count += 1
                except (OSError, FileNotFoundError) as e:
                    print(f"Dosya '{filepath}' temizlenirken hata oluştu: {e}")
                except Exception as e:
                     print(f"Beklenmeyen hata temizlik sırasında: {e}")

    except Exception as e:
        print(f"Temizlik işlemi sırasında genel hata oluştu: {e}")

    print(f"Temizlik tamamlandı. {count} eski dosya kaldırıldı.")
    return count

import atexit
atexit.register(cleanup_old_audio_files, age_seconds=0) # Çıkışta tüm geçici dosyaları sil