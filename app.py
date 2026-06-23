import pandas as pd
import plotly.express as px
import streamlit as st

# 1. Sayfa Ayarları
st.set_page_config(page_title="BistFokus Pro", page_icon="📈", layout="wide")

st.title(" BistFokus Canlı Piyasa Terminali")
st.markdown("**Borsa İstanbul (BIST)** Algoritmik İzleme ve Zaman Serisi Analiz Paneli")
st.divider()

# --- VERİTABANI COĞRAFYASI ---
# DİKKAT: Aşağıdaki tırnak içine KENDİ GOOGLE SHEET ID'Nİ yapıştır!
SHEET_ID = "1jJUkmg5L5mn4MylKoOCKoQxhSH6KEeuXLEJTTU0REvI"
# DİKKAT: Aşağıdaki tırnak içine Sayfa2'nin en sonundaki GID numarasını yapıştır!
SAYFA2_GID = "2082003879"

# Sayfa1 (Ana Tahta) ve Sayfa2 (Zaman Serisi Datası) Linkleri
url_tahta = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"
url_grafik = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={SAYFA2_GID}"

try:
    # Verileri Pandas ile emiyoruz
    df_tahta = pd.read_csv(url_tahta, decimal=",")
    df_grafik = pd.read_csv(url_grafik, decimal=",")
    
    # Tarih sütununu grafik için haritaya düzgünce işliyoruz
    df_grafik['Date'] = pd.to_datetime(df_grafik['Date'])

    # ÜST KISIM: Dinamik Kartlar (Kaç hisse varsa yan yana dizer)
    st.subheader(" Model Portföy Canlı Tahtası")
    
    # Maksimum 4 sütun aç, hisseleri diz
    hisse_sayisi = len(df_tahta)
    cols = st.columns(min(hisse_sayisi, 4))
    
    for i in range(min(hisse_sayisi, 4)):
        with cols[i]:
            h_adi = str(df_tahta.iloc[i]['Hisse'])
            fiyat = float(df_tahta.iloc[i]['Fiyat'])
            degisim = float(df_tahta.iloc[i]['Günlük_Değişim_Yüzde'])
            st.metric(label=f"{h_adi} / Canlı", value=f"{fiyat:,.2f} ₺", delta=f"{degisim:,.2f}%")

    st.write("")
    
    # ALT KISIM: Sol tarafa Tablo, Sağ tarafa TradingView Grafiği
    col_sol, col_sag = st.columns([2, 3]) # %40 sol, %60 sağ bölme
    
    with col_sol:
        st.subheader(" Tahta Listesi")
        st.dataframe(df_tahta, use_container_width=True, hide_index=True)
        st.caption(f"Son Güncelleme: {df_tahta.iloc[0]['Son_Güncelleme']}")

    with col_sag:
        st.subheader(" THYAO 30 Günlük Zaman Serisi")
        
        # Plotly ile fiyakalı borsa çizgisini çiziyoruz
        fig = px.line(
            df_grafik, 
            x="Date", 
            y="Close", 
            labels={"Date": "Tarih", "Close": "Kapanış Fiyatı (₺)"},
            template="plotly_dark" # Sitemizin karanlık moduna tam uyum sağlasın
        )
        
        # Grafiğin renk ve çizgi estetiği
        fig.update_traces(line_color="#2ef2b3", line_width=3)
        fig.update_layout(hovermode="x unified", margin=dict(l=20, r=20, t=20, b=20))
        
        # Ekrana bas
        st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"🚨 Veri akışında kopukluk var! Detay: {e}")