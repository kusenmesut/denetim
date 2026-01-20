import streamlit as st
from utils.db import get_db_connection

def show():
    # --- CSS: İNDİRME KUTUSU TASARIMI ---
    st.markdown("""
    <style>
        /* Kartın Temel Yapısı (Dosya İndirme Alanı Gibi) */
        .download-box {
            background-color: #ffffff;
            border: 2px dashed #f03a73; /* Kesikli Pembe Çizgi */
            border-radius: 20px;
            padding: 40px 20px;
            text-align: center;
            transition: all 0.3s ease;
            cursor: pointer;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 15px;
            height: 100%;
        }

        /* Hover Efekti (Üzerine Gelince) */
        .download-link:hover .download-box {
            background-color: #fff0f5; /* Çok açık pembe zemin */
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(240, 58, 115, 0.15);
            border-style: solid; /* Çizgi düzleşir */
        }

        /* Hayalet İkonu */
        .ghost-icon {
            font-size: 3.5rem;
            animation: float 3s ease-in-out infinite; /* Hafif süzülme efekti */
        }

        /* "Programı İndir" Yazısı */
        .download-text {
            color: #111827;
            font-size: 1.3rem;
            font-weight: 800;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        /* Hover'da yazı rengi */
        .download-link:hover .download-text {
            color: #d81b60;
        }

        /* Alt Bilgi (Sürüm vs.) */
        .download-subtext {
            font-size: 0.9rem;
            color: #9ca3af;
        }

        /* Link Temizleme */
        a.download-link {
            text-decoration: none !important;
            color: inherit !important;
            display: block;
        }

        /* Animasyon */
        @keyframes float {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
            100% { transform: translateY(0px); }
        }
    </style>
    """, unsafe_allow_html=True)

    st.subheader("📊 Sistem Özeti")
    
    # --- METRİKLER ---
    conn = get_db_connection()
    total_users, total_credits, active_scenarios = 0, 0, 0
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM users"); total_users = cur.fetchone()[0]
            cur.execute("SELECT SUM(credits_balance) FROM users"); res = cur.fetchone()[0]; total_credits = res if res else 0
            cur.execute("SELECT COUNT(*) FROM scenarios WHERE is_active=TRUE"); active_scenarios = cur.fetchone()[0]
            conn.close()
        except: pass

    # Metrikleri Göster (Standart Streamlit Metrikleri)
    c1, c2, c3 = st.columns(3)
    c1.metric("👥 Müşteriler", total_users)
    c2.metric("💰 Krediler", f"{total_credits:,}")
    c3.metric("⚡ Senaryolar", active_scenarios)

    # --- ORTADA TEK TIKLANABİLİR İNDİRME KUTUSU ---
    st.write(""); st.write(""); st.write("")

    # Ortalamak için kolon yapısı
    left_col, center_col, right_col = st.columns([1, 2, 1])

    with center_col:
        st.markdown("""
        <a href="https://github.com/kusenmesut/GhostServer/blob/main/aa.zip" target="_blank" class="download-link">
            <div class="download-box">
                <div class="ghost-icon">👻</div>
              
                📥 PROGRAMI İNDİR 📥 
               
                
             
                    Windows • v1.0 • Zip
            
        
        </a>
        """, unsafe_allow_html=True)
