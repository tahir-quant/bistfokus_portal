import pandas as pd
import streamlit as st

st.set_page_config(page_title="BistFokus Pro", page_icon="📈", layout="wide")

st.title(" BistFokus Canlı Piyasa Terminali")
st.markdown("**Borsa İstanbul (BIST)** Algoritmik İzleme Paneli | *Kaynak: Google Finance DB*")
st.divider()

# DİKKAT: Aşağıdaki tırnak içine KENDİ SHEET ID'Nİ yapıştır!
SHEET_ID = "1jJUkmg5L5mn4MylKoOCKoQxhSH6KEeuXLEJTTU0REvI"

csv_url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

try:
    # Virgülü ondalık olarak algıla ve gerisine HİÇ DOKUNMA dedik
    df = pd.read_csv(csv_url, decimal=",")

    st.subheader(" Tahta Özetleri (Canlı)")
    cols = st.columns(4)
    
    with cols[0]:
        hisse_adi = str(df.iloc[0]['Hisse'])
        
        # Sayıları hiçbir string operasyonuna sokmadan, saf matematik objesi olarak çekiyoruz
        fiyat = float(df.iloc[0]['Fiyat'])
        degisim = float(df.iloc[0]['Günlük_Değişim_Yüzde'])
        
        st.metric(
            label=f"{hisse_adi} / Güncel", 
            value=f"{fiyat:,.2f} ₺", 
            delta=f"{degisim:,.2f}%"
        )

    st.write("")
    st.subheader(" Canlı İzleme Listesi")
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.caption(f"Son Veri Eşitleme: {df.iloc[0]['Son_Güncelleme']} (Google Server Time)")

except Exception as e:
    st.error(f"🚨 Veri okuma hatası! Detay: {e}")