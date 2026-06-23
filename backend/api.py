from flask import Flask, jsonify
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/hisseler')
def hisseler():
    # Buraya senin mevcut app.py'deki Google Sheets okuma kodunu kopyala
    url_tahta = "https://docs.google.com/..." # Kendi linkin
    df = pd.read_csv(url_tahta, decimal=",")
    return jsonify({"basari": True, "veriler": df.to_dict(orient="records")})

if __name__ == '__main__':
    app.run()