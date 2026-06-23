from flask import Flask, jsonify
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Senin app.py dosyasındaki orijinal ID'ni kopyaladım
SHEET_ID = "1jJUkmg5L5mn4MylKoOCkoQxhSH6KEeuXLEJTTU0ReVI"

@app.route('/api/hisseler')
def hisseler():
    try:
        url_tahta = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"
        # Render sunucusu Google'dan "bot engeli" yemesin diye sahte tarayıcı kimliği eklendi:
        df = pd.read_csv(url_tahta, decimal=",", storage_options={'User-Agent': 'Mozilla/5.0'})
        return jsonify({"basari": True, "veriler": df.to_dict(orient="records")})
    
    except Exception as e:
        # Eğer yine patlarsa, ekrana 500 hatası yerine hatanın gerçek Türkçe/İngilizce sebebini basacak
        return jsonify({"basari": False, "hata_sebebi": str(e)})

if __name__ == '__main__':
    app.run()