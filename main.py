from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from veri_motoru import borsa_verisi_cek

app = FastAPI(title="BistFokus Canlı Veri Terminali")

# KORSAN KALKANI - "Kimlik sorma" huyunu komple iptal ettik (False), kapıyı herkese açtık (*):
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Dünyadaki herkese izin ver
    allow_credentials=False,  # <--- ZAFERİN KİLİDİ BURASI (True idi, False yaptık!)
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def ana_karsilama():
    return {"mesaj": "BistFokus API Aktif"}


@app.get("/api/hisseler")
def hisseleri_getir():
    return {"basari": True, "veriler": borsa_verisi_cek()}