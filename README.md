# 🎁 Hediye Öneri Botu

Bu proje, kullanıcının hediye almak istediği kişinin özelliklerini (cinsiyet, yaş aralığı, kategori, ilgi alanı) girerek ona uygun hediye önerileri sunan **Streamlit web uygulamasıdır**.


## Özellikler
- Cinsiyet, yaş, kategori ve ilgi alanına göre filtreleme
- Dataset’ten hediye önerisi
- Ürün adı, bağlantısı ve görsel gösterimi
- Tekrar seçim yapma ve ana ekrana dönme özelliği
- Görsel olarak çekici arka plan ve stil


## Teknolojiler
- Python 3
- Streamlit
- Pandas
- base64 (arka plan görseli için)

## Kurulum ve Çalıştırma

#Depoyu klonla ve klasöre gir

```bash
git clone https://github.com/ebrargulsen-code/hediye_oneri.git
cd hediye_oneri

#Sanal ortam oluştur ve aktif et(windows)
python -m venv venv
venv\Scripts\activate


# Gerekli Python paketlerini yükle
pip install -r requirements.txt

# Eğer requirements.txt yoksa manuel yükleyebilirsin
pip install streamlit pandas

# Uygulamayı başlat
streamlit run app.py


