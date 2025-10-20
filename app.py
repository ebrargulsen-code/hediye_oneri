import streamlit as st
import pandas as pd
import random
import base64


#ARKA PLAN FONKSİYONLARI
def get_base_64_of_bin_file(bin_file):
    """Dosyayı base64 formatına çevirir (CSS arka plan için)."""
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        return None


def set_page_bg(png_file):
    """Sayfanın arka planını ayarlar."""
    bin_str = get_base_64_of_bin_file(png_file)
    if bin_str is None:
        st.error(f"Hata: '{png_file}' bulunamadı. Lütfen dosyanın script ile aynı klasörde olduğundan emin ol.")
        return

    page_bg_img = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: cover;
        background-attachment: fixed;
    }}

    h1 {{
        color: #fff;
        text-align: center;
        font-family: 'Comic Sans MS', cursive, sans-serif;
        text-shadow: 2px 2px 6px rgba(0,0,0,0.8);
    }}

    div.stButton > button {{
        background-color: #ff6347;
        color: white;
        font-size: 16px;
        border-radius: 8px;
        padding: 8px 16px;
        border: 2px solid #fff;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
    }}

    div.stSelectbox>div>div {{
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 8px;
        color: #000;
        font-weight: bold;
    }}

    div.stSelectbox p {{
        color: #000 !important;
        font-weight: bold;
    }}

    div[role="listbox"] li {{
        color: #333 !important;
    }}
    div[role="listbox"] li:hover {{
        background-color: #ff6347 !important;
        color: white !important;
    }}

    .result-box {{
        background-color: rgba(255, 255, 255, 0.85);
        padding: 15px;
        border-radius: 10px;
        border: 2px solid #ff6347;
        color: #000;
        margin-top: 10px;
    }}

    .stAlert.stAlertSuccess {{
        background-color: rgba(144, 238, 144, 0.9) !important;
        color: #000 !important;
        font-weight: bold;
        border-radius: 8px;
        padding: 8px 12px;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)


#SAYFA AYARLARI
st.set_page_config(
    page_title="🎁 Hediye Öneri Botu",
    page_icon="🎁",
    layout="centered"
)

# Arka plan yükle
set_page_bg("arkaplan.jpg")

#SAYFA DURUMU (ANA EKRAN / ÖNERİ EKRANI)
if "sayfa" not in st.session_state:
    st.session_state["sayfa"] = "giris"


#ANA EKRAN 
def show_giris_ekrani():
    set_page_bg("arkaplan.jpg")
    st.markdown("<h1>🎁 Hediye Öneri Botu'na Hoş Geldin!</h1>", unsafe_allow_html=True)
    st.markdown("""
    Bu uygulama, hediye almak istediğin kişiye göre sana en uygun hediye önerilerini sunar.  
    Başlamak için aşağıdaki butona tıklayabilirsin. 🚀
    """)
    if st.button("Başla 🚀"):
        st.session_state["sayfa"] = "oneriler"
    st.stop()  # diğer kodları durdurur


#ÖNERİ EKRANI
def show_oneri_ekrani():
    set_page_bg("arkaplan.jpg")
    st.title("🎁 Hediye Öneri Botu")

    try:
        data = pd.read_csv("dataset.csv")

        st.header("Hediye Alacağın Kişi Bilgilerini Seç")

        gender = st.selectbox("Cinsiyet", sorted(data["gender"].unique()))
        category = st.selectbox("Ana Kategori", sorted(data["category"].unique()))

        category_filtered = data[data["category"] == category]
        interest = st.selectbox("İlgi Alanı", sorted(category_filtered["interest"].unique()))

        age_filtered = category_filtered[category_filtered["interest"] == interest]
        age = st.selectbox("Yaş Aralığı", sorted(age_filtered["age"].unique()))

        if st.button("🎁 Öneri Al"):
            filtered = data[
                (data["gender"].str.contains(gender, case=False)) &
                (data["category"] == category) &
                (data["interest"] == interest) &
                (data["age"] == age)
            ]

            if filtered.empty:
                st.warning("Bu kriterlere uygun bir hediye bulunamadı. Lütfen farklı seçimler dene. 😞")
            else:
                product = filtered.sample(1).iloc[0]
                comments = [
                    f"{interest} ile ilgilenen biri için mükemmel bir seçim! 🎯",
                    f"Bu hediye {interest} seven biri için harika olur! 🎁",
                    f"Gerçekten düşünceli bir hediye tercihi! 💡",
                    f"{product['product_name']} kesinlikle çok beğenilecek! 🌟"
                ]
                comment = random.choice(comments)

                st.success("İşte harika bir öneri!")

                # Ürün kutusu
                st.markdown(f"""
                <div class="result-box">
                    <h4>🎁 Önerilen Hediye: {product['product_name']}</h4>
                    <p><em>{comment}</em></p>
                    <a href="{product['link']}" target="_blank"
                       style="text-decoration:none; color:white; background-color:#ff6347;
                       padding:8px 12px; border-radius:8px;">Ürüne Git 🔗</a>
                </div>
                """, unsafe_allow_html=True)

                # Görsel gösterme kısmı
                if 'image_url' in product and pd.notna(product['image_url']):
                    st.image(product['image_url'], width=250, caption=product['product_name'])
                else:
                    st.info("📷 Bu ürün için görsel bulunamadı.")

        # Geri dön butonu
        if st.button("🔙 Ana Ekrana Dön"):
            st.session_state["sayfa"] = "giris"
            st.experimental_rerun()

    except FileNotFoundError:
        st.error("Hata: 'dataset.csv' dosyası bulunamadı. Lütfen dosyanın script ile aynı klasörde olduğundan emin ol.")
    except Exception as e:
        st.error(f"Bir hata oluştu: {e}")


#SAYFA YÖNETİMİ
if st.session_state["sayfa"] == "giris":
    show_giris_ekrani()
else:
    show_oneri_ekrani()
