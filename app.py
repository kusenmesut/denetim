import streamlit as st
import threading
import time
import requests
import urllib3

# --- SAYFA AYARLARI (En başta olmalı) ---
st.set_page_config(page_title="Ghost CFO Office", page_icon="👻", layout="wide")

# --- SSL UYARILARINI GİZLE ---
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- ARKA PLAN UYANDIRMA SERVİSİ (Keep-Alive) ---
# Hedef Sunucu (Senin Render API Adresin)
TARGET_SERVER_URL = "https://ghostserver-rgyz.onrender.com"

@st.cache_resource
def start_keep_alive_service():
    """
    Bu fonksiyon uygulama başladığında SADECE BİR KERE çalışır.
    Arka planda bir 'Daemon Thread' başlatır.
    Bu thread her 30 saniyede bir sunucuya istek atar.
    """
    def run_pinger():
        print("👻 Ghost Pinger Başlatıldı! (Her 30sn)")
        while True:
            try:
                # Sunucuyu dürt (SSL hatasını yoksay, timeout 5sn)
                requests.get(TARGET_SERVER_URL, verify=False, timeout=5)
                # print("💓 Sunucuya sinyal gönderildi.") # Log kirliliği yapmasın diye kapalı
            except Exception as e:
                print(f"⚠️ Ping Hatası: {e}")
            
            # 30 Saniye Bekle (Senin isteğin üzerine)
            time.sleep(30)

    # Arka plan işçisini başlat (daemon=True sayesinde app kapanınca bu da ölür)
    t = threading.Thread(target=run_pinger, daemon=True)
    t.start()

# Servisi Başlat (Sayfa her yenilendiğinde tekrar başlatmaz, cache kullanır)
start_keep_alive_service()

# ========================================================
# --- AŞAĞISI SENİN MEVCUT TASARIM KODLARINDIR ---
# ========================================================

# --- CSS TASARIMI (Görsellerdeki Dark/Pink Teması) ---
st.markdown("""
<style>
    /* 1. ARKA PLAN (Görseldeki Koyu Lacivert/Mor Degrade) */
    .stApp, [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at 50% 0%, #1e1e40 0%, #0b0c1e 60%, #050510 100%) !important;
        color: white !important;
    }

    /* 2. HEADER GİZLEME */
    header[data-testid="stHeader"] {
        background-color: transparent !important;
    }

    /* 3. TİPOGRAFİ (Ortalanmış ve Beyaz) */
    h1 {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 4rem !important;
        text-align: center;
        color: #ffffff !important;
        margin-bottom: 0px !important;
        text-shadow: 0 0 20px rgba(0,0,0,0.5);
    }
    
    h3 {
        font-family: 'Inter', sans-serif;
        font-weight: 300;
        font-size: 1.5rem !important;
        text-align: center;
        color: #cfd8dc !important;
        margin-top: 10px !important;
        margin-bottom: 40px !important;
    }
    
    p {
        text-align: center;
        color: #b0bec5 !important;
        font-size: 1.1rem;
    }

    /* 4. 'GLASS' KARTLAR (İkincil Butonlar) */
    div.stButton > button[kind="secondary"] {
        background-color: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: #ffffff !important;
        height: 140px !important;
        width: 100% !important;
        border-radius: 12px !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }

    div.stButton > button[kind="secondary"]:hover {
        border-color: #f03a73 !important;
        background-color: rgba(255, 255, 255, 0.08) !important;
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(240, 58, 115, 0.2);
    }
    
    div.stButton > button[kind="secondary"]:active {
        background-color: #f03a73 !important;
        color: white !important;
    }

    /* 5. CTA BUTONU (Parlak Pembe) */
    div.stButton > button[kind="primary"] {
        background-color: #f03a73 !important;
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 0.8rem 3rem !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        box-shadow: 0 0 15px rgba(240, 58, 115, 0.4);
        display: block;
        margin: 0 auto;
    }

    div.stButton > button[kind="primary"]:hover {
        background-color: #d81b60 !important;
        box-shadow: 0 0 25px rgba(240, 58, 115, 0.7);
        transform: scale(1.05);
    }

    .nav-container {
        display: flex;
        justify_content: space-between;
        align_items: center;
        padding: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- MEVCUT IMPORTLAR ---
from utils.auth import check_authentication, show_login_page
import register_ui
from views import dashboard, messages, payments, reports, profile, support

# --- LANDING PAGE (YENİ TASARIM) ---
def show_landing_page():
    
    # 1. NAVBAR
    col_logo, col_space, col_login = st.columns([1, 6, 1])
    with col_logo:
        st.markdown("<h3 style='text-align:left !important; margin:0 !important;'>Ghost.</h3>", unsafe_allow_html=True)
    with col_login:
        if st.button("Giriş Yap", key="nav_login", type="primary"):
            st.session_state['page_state'] = 'login'
            st.rerun()

    st.write("") 
    st.write("") 

    # 2. HERO METİNLERİ
    st.markdown("<h1>DENETİM MODÜLÜ DENEME SÜRÜMÜ</h1>", unsafe_allow_html=True)
    st.markdown("<h3>v.1.0.</h3>", unsafe_allow_html=True)
    
    st.write("")
    st.markdown("<p>Bulut Tabanlı Risk ve Denetim Platformu</p>", unsafe_allow_html=True)
    st.write("")

    # 3. KARTLAR (GRID YAPISI)
    c1, c2, c3, c4, c5, c6 = st.columns(6)

    # Emoji kaçış karakterlerini düzelttim (örn: \R -> \\R veya direkt metin)
    with c1:
        if st.button("🔌\nRİSK ANALİZ", key="card_1", type="secondary", use_container_width=True):
            st.session_state['show_register'] = True
            st.session_state['page_state'] = 'register'
            st.rerun()

    with c2:
        if st.button("📑\nMALİ TABLO\nANALİZLERİ", key="card_2", type="secondary", use_container_width=True):
            st.session_state['show_register'] = True
            st.session_state['page_state'] = 'register'
            st.rerun()

    with c3:
        if st.button("📊\nFIRSAT\nANALİZLERİ", key="card_3", type="secondary", use_container_width=True):
            st.session_state['show_register'] = True
            st.session_state['page_state'] = 'register'
            st.rerun()

    with c4:
        if st.button("🔗\nMANUEL DENETİM\nROBOTU", key="card_4", type="secondary", use_container_width=True):
            st.session_state['show_register'] = True
            st.session_state['page_state'] = 'register'
            st.rerun()

    with c5:
        if st.button("☁️\nKİŞİYE ÖZEL\nSENARYOLAR", key="card_5", type="secondary", use_container_width=True):
            st.session_state['show_register'] = True
            st.session_state['page_state'] = 'register'
            st.rerun()
            
    with c6:
        if st.button("💰\nVERİ\nMAHREMİYETİ", key="card_6", type="secondary", use_container_width=True):
            st.session_state['show_register'] = True
            st.session_state['page_state'] = 'register'
            st.rerun()

    st.write("")
    st.write("")
    st.write("")

    # 4. CTA BUTONU
    c_left, c_center, c_right = st.columns([1, 1, 1])
    with c_center:
        if st.button("Ücretsiz Demoyu Başlat →", key="main_cta", type="primary", use_container_width=True):
            st.session_state['show_register'] = True
            st.session_state['page_state'] = 'register'
            st.rerun()

# --- ANA UYGULAMA MANTIĞI ---
def main():
    # 1. State Yönetimi
    if 'page_state' not in st.session_state:
        if not check_authentication():
            st.session_state['page_state'] = 'landing'
        else:
            st.session_state['page_state'] = 'dashboard'

    if 'show_register' not in st.session_state:
        st.session_state.show_register = False

    # 2. Yönlendirme
    state = st.session_state['page_state']

    # -- LANDING PAGE --
    if state == 'landing':
        show_landing_page()

    # -- KAYIT OL --
    elif state == 'register' or st.session_state.show_register:
        st.markdown("<br>", unsafe_allow_html=True)
        col_back, col_rest = st.columns([1, 10])
        with col_back:
            if st.button("←", type="secondary"):
                st.session_state['page_state'] = 'landing'
                st.session_state.show_register = False
                st.rerun()
        register_ui.show()

    # -- GİRİŞ YAP --
    elif state == 'login':
        st.markdown("<br>", unsafe_allow_html=True)
        col_back, col_rest = st.columns([1, 10])
        with col_back:
            if st.button("←", type="secondary"):
                st.session_state['page_state'] = 'landing'
                st.rerun()
        
        if check_authentication():
             st.session_state['page_state'] = 'dashboard'
             st.rerun()
        else:
            show_login_page()

    # -- DASHBOARD --
    elif state == 'dashboard':
        if not check_authentication():
            st.session_state['page_state'] = 'login'
            st.rerun()
            return

        with st.sidebar:
            st.markdown("### Ghost Portal")
            st.markdown(f"👤 **{st.session_state.get('user_name', 'Kullanıcı')}**")
            st.markdown(f"💰 Kredi: **{st.session_state.get('credits', 0)}**")
            st.divider()

            selected_page = st.radio(
                "Menü",
                ["Ana Sayfa", "Raporlarım", "Ödemeler & Kredi", "Mesajlarım", "Profil", "Destek"],
                index=0
            )
            
            st.divider()
            if st.button("Çıkış Yap", type="primary", use_container_width=True):
                st.session_state.clear()
                st.session_state['page_state'] = 'landing'
                st.rerun()

        if selected_page == "Ana Sayfa": dashboard.show()
        elif selected_page == "Raporlarım": reports.show()
        elif selected_page == "Ödemeler & Kredi": payments.show()
        elif selected_page == "Mesajlarım": messages.show()
        elif selected_page == "Profil": profile.show()
        elif selected_page == "Destek": support.show()

if __name__ == "__main__":
    main()
