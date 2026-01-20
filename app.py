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
TARGET_SERVER_URL = "https://ghostserver-rgyz.onrender.com"

@st.cache_resource
def start_keep_alive_service():
    def run_pinger():
        print("👻 Ghost Pinger Başlatıldı! (Her 30sn)")
        while True:
            try:
                requests.get(TARGET_SERVER_URL, verify=False, timeout=5)
            except Exception as e:
                print(f"⚠️ Ping Hatası: {e}")
            time.sleep(30)

    t = threading.Thread(target=run_pinger, daemon=True)
    t.start()

start_keep_alive_service()

# ========================================================
# --- CSS TASARIMI (AÇIK GRİ / MODERN TEMA) ---
# ========================================================
st.markdown("""
<style>
    /* 1. ARKA PLAN (AÇIK GRİ) */
    .stApp, [data-testid="stAppViewContainer"] {
        background-color: #f8f9fa !important;
        color: #1f2937 !important; /* Metin rengi koyu gri/siyah */
    }

    /* 2. HEADER GİZLEME */
    header[data-testid="stHeader"] {
        background-color: transparent !important;
    }

    /* 3. TİPOGRAFİ (Koyu ve Okunaklı) */
    h1 {
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        font-size: 3.5rem !important;
        text-align: center;
        color: #111827 !important; /* Koyu antrasit */
        margin-bottom: 10px !important;
        letter-spacing: -1px;
    }
    
    h3 {
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        font-size: 1.4rem !important;
        text-align: center;
        color: #4b5563 !important; /* Orta gri */
        margin-top: 5px !important;
        margin-bottom: 50px !important;
    }
    
    p {
        text-align: center;
        color: #6b7280 !important;
        font-size: 1.1rem;
    }

    /* 4. KARTLAR (BEYAZ KUTULAR) */
    /* Açık temada beyaz kartlar kullanıyoruz */
    div.stButton > button[kind="secondary"] {
        background-color: #ffffff !important;
        border: 1px solid #e5e7eb !important; /* İnce gri çerçeve */
        color: #374151 !important; /* Koyu gri metin */
        height: 140px !important;
        width: 100% !important;
        border-radius: 16px !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
    }

    /* Hover Efekti: Kart yukarı kalkar ve gölgesi artar */
    div.stButton > button[kind="secondary"]:hover {
        border-color: #f03a73 !important; /* Pembe Kenarlık */
        background-color: #fff0f5 !important; /* Çok hafif pembe zemin */
        color: #111827 !important;
        transform: translateY(-5px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    }
    
    div.stButton > button[kind="secondary"]:active {
        background-color: #f03a73 !important;
        color: white !important;
    }

    /* 5. CTA BUTONU (Parlak Pembe - Değişmedi, kontrast için iyi) */
    div.stButton > button[kind="primary"] {
        background-color: #f03a73 !important;
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 0.8rem 3rem !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 14px 0 rgba(240, 58, 115, 0.39);
        display: block;
        margin: 0 auto;
        transition: transform 0.2s ease-in-out;
    }

    div.stButton > button[kind="primary"]:hover {
        background-color: #d81b60 !important;
        box-shadow: 0 6px 20px rgba(240, 58, 115, 0.23);
        transform: scale(1.05);
    }

    /* 6. LOGO & NAVBAR */
    .ghost-logo {
        color: #111827 !important;
        font-weight: 900;
        font-size: 1.5rem;
    }
    
    /* Yan Menü (Sidebar) Açık Renk Uyumu */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #f3f4f6;
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] p {
        color: #374151 !important;
    }

</style>
""", unsafe_allow_html=True)

# --- MEVCUT IMPORTLAR ---
from utils.auth import check_authentication, show_login_page
import register_ui
from views import dashboard, messages, payments, reports, profile, support

# --- LANDING PAGE (AÇIK TEMA) ---
def show_landing_page():
    
    # 1. NAVBAR
    col_logo, col_space, col_login = st.columns([1, 6, 1])
    with col_logo:
        # Koyu renk logo yazısı (CSS class ile)
        st.markdown("<div class='ghost-logo'>Ghost.</div>", unsafe_allow_html=True)
    with col_login:
        if st.button("Giriş Yap", key="nav_login", type="primary"):
            st.session_state['page_state'] = 'login'
            st.rerun()

    st.write("") 
    st.write("") 
    st.write("") 

    # 2. HERO METİNLERİ
    st.markdown("<h1>DENETİM MODÜLÜ DENEME SÜRÜMÜ</h1>", unsafe_allow_html=True)
    st.markdown("<h3>v.1.0.</h3>", unsafe_allow_html=True)
    
    st.markdown("<p style='font-weight:500;'>Bulut Tabanlı Yeni Nesil Denetim Platformu</p>", unsafe_allow_html=True)
    st.write("")
    st.write("")

    # 3. KARTLAR (GRID YAPISI)
    c1, c2, c3, c4, c5, c6 = st.columns(6)

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
            # Geri butonu için secondary tipinde (artık beyaz kutu)
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
