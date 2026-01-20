import streamlit as st
import hashlib
import time
import datetime
import extra_streamlit_components as stx
from utils.db import get_db_connection

# --- ÇEREZ YÖNETİCİSİ AYARLARI (DÜZELTİLDİ) ---
def get_manager():
    """
    Bu fonksiyon bileşeni ekrana çizer (Render).
    Scriptin her çalışmasında SADECE 1 KEZ çağrılmalıdır.
    """
    # Sabit bir key veriyoruz
    mgr = stx.CookieManager(key="ghost_auth_manager")
    # Oluşturulan bu örneği hafızaya atıyoruz ki diğer fonksiyonlar bunu kullansın
    st.session_state['_active_cookie_manager'] = mgr
    return mgr

def get_existing_manager():
    """
    Bu fonksiyon, zaten çizilmiş olan yöneticiyi getirir.
    Yeni bir tane oluşturmaz (Hata vermemesi için).
    """
    if '_active_cookie_manager' in st.session_state:
        return st.session_state['_active_cookie_manager']
    # Eğer bulunamazsa mecburen yeni oluşturur
    return get_manager()

def hash_password(password):
    """Şifreyi SHA256 ile şifreler."""
    return hashlib.sha256(password.encode()).hexdigest()

def check_authentication():
    """
    Önce Session State'e bakar, yoksa Çerez (Cookie) kontrolü yapar.
    """
    # 1. Oturum zaten açıksa True dön
    if st.session_state.get('authenticated'):
        return True
    
    # 2. Çerez Kontrolü (Beni Hatırla)
    try:
        # Yöneticiyi burada başlatıyoruz (Sayfa başında)
        cookie_manager = get_manager()
        
        # Çerezleri al (Hata önleyici bekleme eklenebilir ama stx genelde hızlıdır)
        cookies = cookie_manager.get_all()
        
        if not cookies:
            return False
            
        auth_token = cookies.get("ghost_user_token") # Çerez adı
        
        if auth_token and "|" in auth_token:
            # Çerez formatı: "email|sifre_hashi"
            saved_email, saved_hash = auth_token.split("|", 1)
            
            # Veritabanından kontrol et
            conn = get_db_connection()
            if conn:
                cur = conn.cursor()
                cur.execute("""
                    SELECT company_name, credits_balance, role, status, password_hash 
                    FROM users WHERE email=%s
                """, (saved_email,))
                user = cur.fetchone()
                cur.close()
                conn.close()
                
                if user:
                    db_hash = user[4]
                    db_status = str(user[3]).strip().capitalize()
                    
                    if db_hash == saved_hash and db_status == 'Aktif':
                        st.session_state.authenticated = True
                        st.session_state.user_name = user[0]
                        st.session_state.credits = user[1]
                        st.session_state.role = user[2]
                        st.session_state.email = saved_email
                        return True
    except Exception as e:
        print(f"Çerez hatası: {e}")
        
    return False

def login_user(email, password, remember_me=False):
    """Kullanıcı girişi."""
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            pass_hash = hash_password(password)
            
            cur.execute("""
                SELECT company_name, credits_balance, role, status 
                FROM users 
                WHERE email=%s AND password_hash=%s
            """, (email, pass_hash))
            
            user = cur.fetchone()
            cur.close()
            conn.close()
            
            if user:
                status_clean = str(user[3]).strip().capitalize()
                
                if status_clean != 'Aktif':
                    return False, "Hesabınız pasif durumda."
                    
                st.session_state.authenticated = True
                st.session_state.user_name = user[0]
                st.session_state.credits = user[1]
                st.session_state.role = user[2]
                st.session_state.email = email
                
                # --- BENİ HATIRLA (GÜNCELLENDİ) ---
                if remember_me:
                    # BURADA get_manager DEĞİL, get_existing_manager KULLANIYORUZ
                    cookie_manager = get_existing_manager()
                    
                    token_val = f"{email}|{pass_hash}"
                    expires = datetime.datetime.now() + datetime.timedelta(days=7)
                    
                    # Çerezi ayarla
                    cookie_manager.set("ghost_user_token", token_val, expires_at=expires)
                # ----------------------------------
                
                return True, "Giriş Başarılı"
            else:
                return False, "E-posta veya şifre hatalı."
        except Exception as e:
            return False, f"Hata: {e}"
    return False, "Veritabanı bağlantısı yok."

def change_user_password(email, new_password):
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            new_hash = hash_password(new_password)
            cur.execute("UPDATE users SET password_hash = %s WHERE email = %s", (new_hash, email))
            conn.commit()
            cur.close()
            conn.close()
            return True, "Şifre güncellendi."
        except Exception as e:
            return False, f"DB Hatası: {e}"
    return False, "Bağlantı hatası."

def show_login_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("https://cdn-icons-png.flaticon.com/512/2919/2919600.png", width=80)
        st.title("Ghost Giriş")
        
        email = st.text_input("E-Posta")
        password = st.text_input("Şifre", type="password")
        remember = st.checkbox("Beni Hatırla")
        
        c_log, c_reg = st.columns(2)
        
        if c_log.button("Giriş Yap", type="primary", use_container_width=True):
            if not email or not password:
                st.warning("Lütfen alanları doldurunuz.")
            else:
                success, msg = login_user(email, password, remember)
                if success:
                    st.success("Giriş Başarılı!")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error(msg)
        
        if c_reg.button("✨ Kayıt Ol", use_container_width=True):
            st.session_state.show_register = True
            st.rerun()

        st.markdown("---")
        if st.button("❓ Şifremi Unuttum"):
            st.info("Yönetici ile iletişime geçin.")