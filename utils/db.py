import streamlit as st
import pandas as pd
import os
from sqlalchemy import create_engine, text

# .env desteği
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

def get_db_url():
    """
    Önce .env dosyasındaki DATABASE_URL'ye bakar.
    Bulamazsa st.secrets içindeki ayarlara bakar.
    """
    # 1. Seçenek: Çevre Değişkeni
    url = os.getenv("DATABASE_URL")
    if url:
        return url.replace("postgres://", "postgresql://")
    
    # 2. Seçenek: Streamlit Secrets
    if "connections" in st.secrets and "postgresql" in st.secrets["connections"]:
        try:
            cfg = st.secrets["connections"]["postgresql"]
            return f"postgresql+psycopg2://{cfg['username']}:{cfg['password']}@{cfg['host']}:{cfg['port']}/{cfg['database']}"
        except:
            pass
            
    return None

def get_db_engine():
    """Pandas işlemleri için SQLAlchemy Engine döndürür."""
    url = get_db_url()
    if not url:
        st.error("🚨 Veritabanı bağlantı adresi bulunamadı.")
        return None
    
    try:
        engine = create_engine(url)
        return engine
    except Exception as e:
        st.error(f"Engine Hatası: {e}")
        return None

def get_db_connection():
    """
    INSERT/UPDATE/DELETE için HAM (Raw) bağlantı döndürür.
    Bu sayede .cursor() metodu sorunsuz çalışır.
    """
    engine = get_db_engine()
    if engine:
        try:
            # GÖNDERDİĞİNİZ KRİTİK DÜZELTME:
            return engine.raw_connection()
        except Exception as e:
            st.error(f"Bağlantı Hatası: {e}")
            return None
    return None
