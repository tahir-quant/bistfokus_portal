import urllib.request
import io
import csv

# ⚠️ DİKKAT: Kendi Google Sheet ID Anahtarını buradaki tırnağın içine TEKRAR yapıştır!
TABLO_ID = "1jJUkmg5L5mn4MylKoOCKoQxhSH6KEeuXLEJTTU0REvI"

URL = f"https://docs.google.com/spreadsheets/d/{TABLO_ID}/export?format=csv"

def borsa_verisi_cek():
    """Google Sheet'teki veriyi Excel tablosu gibi okuyup 'Sözlük (JSON)' formatına çevirir."""
    try:
        istek = urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(istek) as cevap:
            veri_ham = cevap.read().decode('utf-8')
            
        okuyucu = csv.reader(io.StringIO(veri_ham))
        satirlar = list(okuyucu)
        
        # Eğer tablo boşsa veya sadece başlık varsa boş liste dön
        if not satirlar or len(satirlar) < 2:
            return []
        
        basliklar = satirlar[0]  # ['Hisse', 'Fiyat', 'Günlük_Değişim_Yüzde', 'Hacim', 'Son_Güncelleme']
        sonuc_listesi = []
        
        for satir in satirlar[1:]:
            # zip() komutu, Sütun Başlığı ile Satır Verisini fermuar gibi birbirine diker!
            # Örn: {'Hisse': 'THYAO', 'Fiyat': '312.5'}
            hisse_objesi = dict(zip(basliklar, satir))
            sonuc_listesi.append(hisse_objesi)
            
        return sonuc_listesi

    except Exception as hata:
        return [{"Hata": f"Veri okunamadı. Detay: {str(hata)}"}]