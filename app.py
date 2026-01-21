import streamlit as st
import threading
import time
import requests
import urllib3

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Ghost CFO Office", page_icon="👻", layout="wide")

# --- SSL UYARILARINI GİZLE ---
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- MEVCUT IMPORTLAR ---
try:
    from utils.auth import check_authentication, show_login_page
    import register_ui
    from views import dashboard, messages, payments, reports, profile, support
except ImportError as e:
    st.error(f"Modül Hatası: {e}")
    st.stop()

# --- SUNUCU AYARLARI ---
TARGET_SERVER_URL = "https://ghostserver-rgyz.onrender.com"

# --- UYANDIRMA SERVİSİ ---
@st.cache_resource
def start_keep_alive_service():
    def run_pinger():
        while True:
            try:
                requests.get(TARGET_SERVER_URL, verify=False, timeout=5)
            except: pass
            time.sleep(30)
    threading.Thread(target=run_pinger, daemon=True).start()

start_keep_alive_service()

# --- URL VE OTURUM YÖNETİMİ (KESİN ÇÖZÜM) ---

def restore_session_from_url():
    """
    URL'de kullanıcı adı varsa, sunucuya sormadan oturumu açar.
    Bu fonksiyon F5 yapıldığında çalışır.
    """
    query_params = st.query_params
    url_user = query_params.get("user", None)
    
    # Eğer oturum yok ama URL'de kullanıcı adı varsa -> İÇERİ AL
    if 'authenticated' not in st.session_state and url_user:
        st.session_state['authenticated'] = True
        st.session_state['user_name'] = url_user
        # Token ve kredi bilgisi opsiyonel, hata vermemesi için dummy veriyoruz
        st.session_state['token'] = "demo_token" 
        st.session_state['credits'] = "∞" 
        return True
    return False

def go_to(page, user=None):
    """
    Sayfa değiştirirken URL'ye kullanıcı adını da ekler.
    Böylece F5 atınca sistem seni hatırlar.
    """
    st.session_state['page_state'] = page
    
    params = {"page": page}
    
    # Kullanıcı adını bul ve URL'ye yapıştır
    current_user = user or st.session_state.get('user_name')
    if current_user:
        params["user"] = current_user
        
    st.query_params.clear()
    st.query_params.update(params)
    st.rerun()

# ========================================================
# --- CSS TASARIMI (AÇIK GRİ / MODERN TEMA) ---
# ========================================================
st.markdown("""
<style>
    .stApp, [data-testid="stAppViewContainer"] { background-color: #f8f9fa !important; color: #1f2937 !important; }
    header[data-testid="stHeader"] { background-color: transparent !important; }
    h1 { font-family: 'Inter', sans-serif; font-weight: 800; font-size: 3.5rem !important; text-align: center; color: #111827 !important; letter-spacing: -1px; }
    h3 { font-family: 'Inter', sans-serif; font-weight: 500; font-size: 1.4rem !important; text-align: center; color: #4b5563 !important; }
    div.stButton > button[kind="secondary"] { background-color: #ffffff !important; border: 1px solid #e5e7eb !important; color: #374151 !important; height: 140px !important; width: 100% !important; border-radius: 16px !important; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); }
    div.stButton > button[kind="secondary"]:hover { border-color: #f03a73 !important; background-color: #fff0f5 !important; transform: translateY(-5px); }
    div.stButton > button[kind="primary"] { background-color: #f03a73 !important; color: white !important; border: none !important; border-radius: 50px !important; padding: 0.8rem 3rem !important; display: block; margin: 0 auto; }
    div.stButton > button[kind="primary"]:hover { background-color: #d81b60 !important; transform: scale(1.05); }
    .ghost-logo { color: #111827 !important; font-weight: 900; font-size: 1.5rem; }
    [data-testid="stSidebar"] { background-color: #ffffff !important; border-right: 1px solid #f3f4f6; }
    [data-testid="stSidebar"] * { color: #374151 !important; }
</style>
""", unsafe_allow_html=True)

# --- LANDING PAGE ---
def show_landing_page():
    col_logo, _, col_login = st.columns([1, 6, 1])
    with col_logo: st.markdown("<div class='ghost-logo'>Ghost.</div>", unsafe_allow_html=True)
    with col_login:
        if st.button("Giriş Yap", key="nav_login", type="primary"): go_to('login')

    st.write(""); st.write(""); st.write("") 
    st.markdown("<h1>DENETİM MODÜLÜ DENEME SÜRÜMÜ</h1>", unsafe_allow_html=True)
    st.markdown("<h3>v.1.0.</h3>", unsafe_allow_html=True)
    st.markdown("<p style='font-weight:500; text-align:center;'>Bulut Tabanlı Yeni Nesil Denetim Platformu</p>", unsafe_allow_html=True)
    st.write(""); st.write("")

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    buttons = [
        (c1, "🔌\nRİSK ANALİZ"), (c2, "📑\nMALİ TABLO\nANALİZLERİ"), 
        (c3, "📊\nFIRSAT\nANALİZLERİ"), (c4, "🔗\nMANUEL DENETİM\nROBOTU"),
        (c5, "☁️\nKİŞİYE ÖZEL\nSENARYOLAR"), (c6, "💰\nVERİ\nMAHREMİYETİ")
    ]
    for col, text in buttons:
        with col:
            if st.button(text, key=f"card_{text}", type="secondary", use_container_width=True): go_to('register')

    st.write(""); st.write("")
    _, c_center, _ = st.columns([1, 1, 1])
    with c_center:
        if st.button("Ücretsiz Demoyu Başlat →", key="main_cta", type="primary", use_container_width=True): go_to('register')

# --- ANA UYGULAMA MANTIĞI ---
def main():
    # 1. URL KONTROLÜ (F5 KURTARMA OPERASYONU)
    # Önce URL'den kullanıcı adı var mı diye bakıp session'ı zorla dolduruyoruz
    restore_session_from_url()

    # Sayfa Durumunu Belirle
    if 'page_state' not in st.session_state:
        query_params = st.query_params
        url_page = query_params.get("page", "landing")
        
        # Eğer dashboard isteniyorsa ama session hala yoksa login'e at
        if url_page == "dashboard" and 'authenticated' not in st.session_state:
            url_page = "login"
            
        st.session_state['page_state'] = url_page

    if 'show_register' not in st.session_state: st.session_state.show_register = False

    # 2. YÖNLENDİRME
    state = st.session_state['page_state']

    if state == 'landing':
        show_landing_page()

    elif state == 'register':
        st.markdown("<br>", unsafe_allow_html=True)
        c1, _ = st.columns([1, 10])
        with c1:
            if st.button("←", type="secondary"): go_to('landing')
        register_ui.show()

    elif state == 'login':
        st.markdown("<br>", unsafe_allow_html=True)
        c1, _ = st.columns([1, 10])
        with c1:
            if st.button("←", type="secondary"): go_to('landing')
        
        # Eğer zaten giriş yapmışsa direkt dashboard'a at
        if st.session_state.get('authenticated'):
             go_to('dashboard')
        else:
            show_login_page()
            # Login butonuna basıldıktan hemen sonra kontrol et
            if st.session_state.get('authenticated'):
                # Kullanıcı adını almayı dene, yoksa varsayılan ata
                user = st.session_state.get('user_name', 'Kullanici')
                go_to('dashboard', user=user)

    elif state == 'dashboard':
        # Güvenlik (Ama restore_session_from_url sayesinde burası F5'te geçilecek)
        if not st.session_state.get('authenticated'):
            go_to('login')
            return

        # Sidebar
        with st.sidebar:
            st.markdown("### Ghost Portal")
            st.markdown(f"👤 **{st.session_state.get('user_name', 'Kullanıcı')}**")
            st.markdown(f"💰 Kredi: **{st.session_state.get('credits', '∞')}**")
            st.divider()

            selected_page = st.radio("Menü", ["Ana Sayfa", "Raporlarım", "Ödemeler & Kredi", "Mesajlarım", "Profil", "Destek"], index=0)
            st.divider()
            
            if st.button("Çıkış Yap", type="primary", use_container_width=True):
                st.session_state.clear()
                st.query_params.clear() 
                go_to('landing')

        # İçerik
        if selected_page == "Ana Sayfa": dashboard.show()
        elif selected_page == "Raporlarım": reports.show()
        elif selected_page == "Ödemeler & Kredi": payments.show()
        elif selected_page == "Mesajlarım": messages.show()
        elif selected_page == "Profil": profile.show()

# 2. Uyandırma Fonksiyonunu Tanımla
def wake_up_server_job():
    """
    Uygulama çalıştırıldığı an Render sunucusuna 'Uyan' sinyali gönderir.
    GUI yüklenirken sunucu arkada ısınmış olur.
    """
    TARGET_URL = "https://ghostserver-rgyz.onrender.com"
    try:
        # verify=False: SSL hatasını yoksay
        # timeout=3: 3 saniye içinde cevap gelmezse işlemi sal (Uygulamayı yavaşlatma)
        requests.get(TARGET_URL, timeout=3, verify=False)
        print("🚀 Sunucu uyandırma sinyali gönderildi (Background).")
    except Exception as e:
        # İnternet yoksa veya sunucu hatası varsa sessizce geç
        pass

# 3. İŞTE BURASI: Uygulama Başlamadan Hemen Önce Thread Başlat
# Bu satır root = tk.Tk() satırından ÖNCE gelmeli.
threading.Thread(target=wake_up_server_job, daemon=True).start()


if __name__ == "__main__":
    main()

