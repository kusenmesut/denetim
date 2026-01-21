
import streamlit as st
from utils.db import get_db_connection

    
def show():
    # --- CSS: KART VE İNDİRME KUTUSU TASARIMLARI ---
    st.markdown("""
    <style>
        /* --- MEVCUT METRİK KARTLARI STİLLERİ --- */
        .dashboard-card {
            background-color: #ffffff;
            border: 1px solid #e5e7eb;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            transition: transform 0.2s;
            margin-bottom: 10px;
        }
        .dashboard-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        }
        .metric-title {
            color: #6b7280;
            font-size: 0.9rem;
            font-weight: 600;
            margin-bottom: 5px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        .metric-value {
            color: #111827;
            font-size: 2rem;
            font-weight: 800;
        }
        .metric-icon {
            font-size: 1.8rem;
            margin-bottom: 10px;
            background-color: #f3f4f6;
            width: 50px;
            height: 50px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 10px;
        }

        /* --- YENİ EKLENEN: ORTADAKİ DEV İNDİRME KUTUSU --- */

        /* 1. Link Kapsayıcısı (Tıklanabilir Alan) */
        .big-download-link {
            text-decoration: none !important; /* Alt çizgiyi kaldır */
            color: inherit !important; /* Rengi koru */
            display: flex;
            justify-content: center; /* Yatayda ortala */
            margin-top: 50px;
            margin-bottom: 30px;
            perspective: 1000px; /* 3D efekt için derinlik */
        }

        /* 2. Kare Kutu Tasarımı */
        .big-ghost-box {
            width: 350px;  /* Karenin genişliği */
            height: 350px; /* Karenin yüksekliği */
            background: linear-gradient(145deg, #ffffff, #f8f9fa); /* Hafif gradyan arka plan */
            border: 4px solid #e5e7eb; /* Kalın gri çerçeve */
            border-radius: 30px; /* Yuvarlak köşeler */
            display: flex;
            flex-direction: column;
            align-items: center; /* İçeriği yatay ortala */
            justify-content: center; /* İçeriği dikey ortala */
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); /* Yaylı geçiş efekti */
            cursor: pointer;
        }

        /* 3. Hover (Üzerine Gelince) Efektleri */
        .big-download-link:hover .big-ghost-box {
            border-color: #f03a73; /* Çerçeve pembe olsun (Marka rengin) */
            transform: translateY(-15px) scale(1.03); /* Yukarı kalk ve hafif büyü */
            box-shadow: 0 30px 60px -12px rgba(240, 58, 115, 0.25); /* Pembe gölge */
        }

        /* 4. Dev Hayalet Emojisi */
        .giant-ghost-emoji {
            font-size: 10rem; /* Çok büyük boyut */
            line-height: 1;
            margin-bottom: 20px;
            filter: drop-shadow(0 10px 10px rgba(0,0,0,0.1));
            transition: transform 0.4s ease;
        }

        /* Hover'da Hayalet Hareketi */
        .big-download-link:hover .giant-ghost-emoji {
            transform: scale(1.1) rotate(-10deg); /* Büyü ve hafif dön */
        }

        /* 5. Alt Yazı */
        .download-action-text {
            font-size: 1.8rem;
            font-weight: 900;
            color: #111827;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        /* Hover'da yazı rengi */
        .big-download-link:hover .download-action-text {
            color: #f03a73;
        }
    </style>
    """, unsafe_allow_html=True)

    
    # --- VERİLERİ HAZIRLA (Varsayılan 0) ---
    total_users = 0
    total_credits = 0
    active_scenarios = 0
    
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            
            # 1. Toplam Kullanıcı
            cur.execute("SELECT COUNT(*) FROM users") 
            row_users = cur.fetchone()
            if row_users: total_users = row_users[0]
            
            # 2. Toplam Kredi
            cur.execute("SELECT SUM(credits_balance) FROM users")
            row_credits = cur.fetchone()
            if row_credits and row_credits[0]: total_credits = row_credits[0]
            
            # 3. Aktif Senaryolar
            cur.execute("SELECT COUNT(*) FROM scenarios WHERE is_active=TRUE")
            row_scenarios = cur.fetchone()
            if row_scenarios: active_scenarios = row_scenarios[0]
            
            conn.close()
        except Exception as e:
            st.error(f"Veri çekme hatası: {e}")
    
  

    st.title("📊 İstatistikler")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Toplam Rapor", "0")
    c2.metric("Kredi", str(st.session_state.get('credits',0)))
    c3.metric("Aktif Cihaz", "1")
    c4.metric("Durum", "Aktif")
    st.success("Veritabanı ve Oturum entegrasyonu başarılı!")
    st.markdown("""
    <a href="https://github.com/kusenmesut/denetim/raw/main/app.zip" class="big-download-link">
        <div class="big-ghost-box">
            <div class="giant-ghost-emoji">👻</div>
            <div class="download-action-text">DOSYAYI İNDİR</div>
        </div>
    </a>
    """, unsafe_allow_html=True)