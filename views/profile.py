import streamlit as st
from utils.auth import change_user_password

def show():
    st.title("👤 Profil Ayarları")
    st.markdown("Hesap bilgilerinizi görüntüleyebilir ve şifrenizi güncelleyebilirsiniz.")
    
    # --- KULLANICI BİLGİ KARTI ---
    with st.container(border=True):
        c1, c2 = st.columns(2)
        c1.text_input("Firma Ünvanı", value=st.session_state.get('user_name', ''), disabled=True)
        c2.text_input("E-Posta Adresi", value=st.session_state.get('email', ''), disabled=True)
        st.caption("ℹ️ Firma ve E-posta değişiklikleri için yönetici ile iletişime geçiniz.")

    st.markdown("---")

    # --- ŞİFRE DEĞİŞTİRME ALANI ---
    st.subheader("🔐 Şifremi Değiştir")
    
    with st.form("password_change_form"):
        col_p1, col_p2 = st.columns(2)
        
        with col_p1:
            new_pass = st.text_input("Yeni Şifre", type="password", placeholder="Yeni şifrenizi girin")
        
        with col_p2:
            confirm_pass = st.text_input("Yeni Şifre (Tekrar)", type="password", placeholder="Şifreyi tekrar girin")
            
        btn_update = st.form_submit_button("Şifreyi Güncelle", type="primary")
        
        if btn_update:
            if not new_pass or not confirm_pass:
                st.warning("Lütfen her iki şifre alanını da doldurunuz.")
            elif new_pass != confirm_pass:
                st.error("❌ Şifreler birbiriyle eşleşmiyor.")
            elif len(new_pass) < 4:
                st.warning("⚠️ Şifre en az 4 karakter olmalıdır.")
            else:
                # E-posta session'dan alınıyor
                user_email = st.session_state.get('email')
                
                if user_email:
                    success, msg = change_user_password(user_email, new_pass)
                    if success:
                        st.success(f"✅ {msg}")
                    else:
                        st.error(f"❌ {msg}")
                else:
                    st.error("Oturum hatası: E-posta bilgisi bulunamadı. Lütfen çıkış yapıp tekrar girin.")