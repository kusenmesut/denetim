import streamlit as st
import time
from utils.db import get_db_connection
from utils.auth import hash_password 

def check_email_exists(email):
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT count(*) FROM users WHERE email = %s", (email,))
            count = cur.fetchone()[0]
            cur.close()
            conn.close()
            return count > 0
        except: return False
    return False

def show():
    # Geri Butonu: Landing yerine Giriş Ekranına dönsün istersen 'login' yapabilirsin
    if st.button("← Giriş Ekranına Dön"):
        st.session_state['page_state'] = 'login'
        st.session_state.show_register = False
        st.query_params["page"] = "login" # URL'yi güncelle
        st.rerun()

    st.title("👻 Yeni Hesap Oluştur")
    with st.form("register_form"):
        col1, col2 = st.columns(2)
        with col1:
            company_name = st.text_input("Firma Ünvanı")
            email = st.text_input("E-Posta Adresi")
        with col2:
            password = st.text_input("Şifre", type="password")
            password_confirm = st.text_input("Şifre (Tekrar)", type="password")

        submitted = st.form_submit_button("🚀 Kaydı Tamamla", type="primary", use_container_width=True)

        if submitted:
            if not company_name or not email or not password:
                st.warning("Lütfen tüm alanları doldurunuz.")
                return
            if password != password_confirm:
                st.error("Şifreler eşleşmiyor.")
                return
            if check_email_exists(email):
                st.error("Bu e-posta adresi zaten kayıtlı.")
                return

            try:
                conn = get_db_connection()
                if conn:
                    cur = conn.cursor()
                    pass_hash = hash_password(password)
                    # Varsayılan rol 'user', durum 'Aktif'
                    sql = "INSERT INTO users (email, password_hash, company_name, credits_balance, role, status, max_device_limit) VALUES (%s, %s, %s, 0, 'user', 'Aktif', 1)"
                    cur.execute(sql, (email, pass_hash, company_name))
                    conn.commit()
                    cur.close()
                    conn.close()
                    
                    st.success("✅ Kayıt Başarılı! Giriş ekranına yönlendiriliyorsunuz...")
                    time.sleep(1.5) # Kullanıcının mesajı görmesi için kısa bekleme
                    
                    # --- YÖNLENDİRME KISMI ---
                    st.session_state['page_state'] = 'login'  # Sayfa durumunu 'login' yap
                    st.session_state.show_register = False    # Kayıt modunu kapat
                    st.query_params["page"] = "login"         # URL'yi güncelle (F5 koruması için)
                    st.rerun()                                # Sayfayı yenile
                    
                else:
                    st.error("Veritabanı bağlantı hatası.")
            except Exception as e:
                st.error(f"Hata: {e}")
