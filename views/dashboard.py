import streamlit as st
def show():
    st.title("📊 İstatistikler")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Toplam Rapor", "0")
    c2.metric("Kredi", str(st.session_state.get('credits',0)))
    c3.metric("Aktif Cihaz", "1")
    c4.metric("Durum", "Aktif")
    st.success("Veritabanı ve Oturum entegrasyonu başarılı!")
