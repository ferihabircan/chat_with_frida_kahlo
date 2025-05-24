

# 💃🎨🥀 Frida Kahlo AI Chatbot 🖌️🌵🇲🇽

![Frida Kahlo Illustration](https://upload.wikimedia.org/wikipedia/commons/thumb/0/06/Frida_Kahlo%2C_by_Guillermo_Kahlo.jpg/440px-Frida_Kahlo%2C_by_Guillermo_Kahlo.jpg)

¡Hola, mis amores! 👋 Bu proje, Meksika'nın tutkulu ve ikonik sanatçısı Frida Kahlo'nun ruhunu dijital dünyaya taşıyan bir yapay zeka sohbet deneyimidir. 💃🌹 Metinlerinize yanıt veren, onun sanatından, hayatından ve Diego'sundan bahseden bir Frida ile sohbet edin. Üstelik, cevaplarını kendi sesiyle dinleyin! 🗣️👂 (Seslendirme, Eleven Labs teknolojisi ile güçlendirilmiştir ✨). Gradio sayesinde, bu deneyimi kolayca web arayüzü üzerinden yaşayabilirsiniz.

## ✨ Neden Frida Chatbot?

-   **Gerçekçi Sohbet:** Google Gemini'nin gücüyle Frida'nın üslubuna yakın yanıtlar alın. 🧠💬
-   **Sesli Yanıtlar:** Eleven Labs'in yüksek kaliteli seslendirmesi ile Frida'yı duyma fırsatı yakalayın. 🗣️🎧
-   **Kullanıcı Dostu Arayüz:** Gradio'nun basit arayüzü ile kolayca sohbet edin ve etkileşim kurun.🖱️✨
-   **Temizlik Yönetimi:** Geçici ses dosyaları otomatik olarak yönetilir. 🧹🎶

## 🚀 Kurulum ve Çalıştırma

Frida ile sohbet etmek için aşağıdaki basit adımları izleyin:

1.  **Depoyu Klonlayın:** Bilgisayarınıza indirin.
    ```bash
    git clone https://github.com/KULLANICIADINIZ/DEPOADINIZ.git
    cd DEPOADINIZ # 📁 Proje klasörüne gidin
    ```
    *(`KULLANICIADINIZ/DEPOADINIZ.git` kısmını kendi depo adresinizle değiştirin.)*

2.  **Sanal Ortam Oluşturun:** Proje için temiz bir çalışma alanı hazırlayın. 📦
    ```bash
    python -m venv venv
    ```

3.  **Sanal Ortamı Aktif Edin:** Hazırladığınız ortama girin. 🚪
    -   Windows:
        ```bash
        .\venv\Scripts\activate
        ```
    -   macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

4.  **Bağımlılıkları Yükleyin:** Projenin çalışması için gerekli tüm kütüphaneleri edinin. 📚
    ```bash
    pip install -r requirements.txt
    ```
    *(Eğer `requirements.txt` dosyanız yoksa, venv aktifken `pip freeze > requirements.txt` komutunu çalıştırıp sonra tekrar deneyin.)*

5.  **API Anahtarlarını Ayarlayın:** Yapay zeka ve seslendirme servisleri için anahtarlarınızı girin. 🔑🔒
    Projenin ana dizininde `.env` adında bir dosya oluşturun ve içine aşağıdaki satırları ekleyin:
    ```dotenv
    GOOGLE_API_KEY=YOUR_GEMINI_API_KEY_HERE
    ELEVENLABS_API_KEY=YOUR_ELEVEN_LABS_API_KEY_HERE
    ```
    `YOUR_GEMINI_API_KEY_HERE` ve `YOUR_ELEVEN_LABS_API_KEY_HERE` kısımlarını kendi API anahtarlarınızla değiştirin.
    *(🚨 **Güvenlik Uyarısı:** `.env` dosyanızı **ASLA** Git'e eklemeyin! `.gitignore` dosyanızda `.env` satırı olduğundan emin olun.)*

6.  **Frida'yı Başlatın!** 🎉
    Sanal ortamınız aktifken proje dizininde şu komutu çalıştırın:
    ```bash
    python app.py
    ```
    Uygulama başlayacak ve size bir yerel adres verecektir. 🌐 Tarayıcınızı açın ve bu adrese gidin.



