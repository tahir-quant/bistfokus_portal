"use client";

import { useEffect, useState } from "react";
import { TrendingUp, TrendingDown, RefreshCw, BarChart3, Activity } from "lucide-react";

interface HisseVeri {
  Hisse: string;
  Fiyat: string;
  Günlük_Değişim_Yüzde: string;
  Hacim: string;
  Son_Güncelleme: string;
}

export default function Home() {
  const [veriler, setVeriler] = useState<HisseVeri[]>([]);
  const [yukleniyor, setYukleniyor] = useState(true);
  const [sonYenileme, setSonYenileme] = useState("");

  const veriyiCek = async () => {
    setYukleniyor(true);
    try {
      const res = await fetch(https://bistfokus-backend.onrender.com/api/hisseler);
      const data = await res.json();
      if (data.basari) {
        setVeriler(data.veriler);
        const simdi = new Date();
        setSonYenileme(simdi.toLocaleTimeString("tr-TR"));
      }
    } catch (hata) {
      console.error("API Bağlantı Hatası:", hata);
    } finally {
      setYukleniyor(false);
    }
  };

  useEffect(() => {
    veriyiCek();
  }, []);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-4 md:p-10 font-sans">
      {/* Üst Bar (Header) */}
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-start md:items-center border-b border-slate-800 pb-6 mb-8 gap-4">
        <div>
          <div className="flex items-center gap-3 font-mono">
            <div className="h-3 w-3 rounded-full bg-emerald-500 animate-pulse" />
            <h1 className="text-2xl md:text-3xl font-black tracking-tighter bg-gradient-to-r from-emerald-400 to-teal-200 bg-clip-text text-transparent">
              BISTFOKUS<span className="text-slate-500 font-light">.PRO</span>
            </h1>
          </div>
          <p className="text-slate-400 text-xs mt-1 font-mono">
            Google Sheets & Python Destekli Canlı Algoritmik Portföy Ekranı
          </p>
        </div>

        <div className="flex items-center gap-3 w-full md:w-auto justify-between">
          <span className="text-xs text-slate-500 font-mono bg-slate-900 px-3 py-1.5 rounded-md border border-slate-800">
            Son Veri: {sonYenileme || "Senkronize ediliyor..."}
          </span>
          <button
            onClick={veriyiCek}
            disabled={yukleniyor}
            className="flex items-center gap-2 bg-emerald-600 hover:bg-emerald-500 text-white px-4 py-2 rounded-lg font-medium text-xs transition-all shadow-lg shadow-emerald-950 disabled:opacity-50"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${yukleniyor ? "animate-spin" : ""}`} />
            <span>Yenile</span>
          </button>
        </div>
      </div>

      {/* Ana Veri Izgarası (Grid) */}
      <div className="max-w-7xl mx-auto">
        {yukleniyor && veriler.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-64 gap-3 text-slate-500 font-mono text-sm">
            <Activity className="w-8 h-8 animate-spin text-emerald-500" />
            <p>BIST Verileri Google Finance Tulumbasından Emiliyor...</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
            {veriler.map((item, index) => {
              // Değişim oranını matematiksel sayıya çevir (Örn: "0,62" -> 0.62)
              const degisimFloat = parseFloat(item.Günlük_Değişim_Yüzde?.replace(",", ".") || "0");
              const artismi = degisimFloat >= 0;

              return (
                <div
                  key={index}
                  className="bg-slate-900/50 border border-slate-800 rounded-xl p-5 hover:border-slate-700 transition-all hover:shadow-2xl hover:shadow-emerald-950/20 flex flex-col justify-between group"
                >
                  {/* Kart Üst: Hisse Adı & Trend İkonu */}
                  <div className="flex justify-between items-start mb-3">
                    <div>
                      <h3 className="text-2xl font-black tracking-tight text-white group-hover:text-emerald-400 transition-colors">
                        {item.Hisse}
                      </h3>
                      <span className="text-[10px] text-slate-500 font-mono tracking-wider">BIST 100</span>
                    </div>
                    <div
                      className={`p-2 rounded-lg ${
                        artismi
                          ? "bg-emerald-950/60 text-emerald-400 border border-emerald-800/60"
                          : "bg-rose-950/60 text-rose-400 border border-rose-800/60"
                      }`}
                    >
                      {artismi ? <TrendingUp className="w-4 h-4" /> : <TrendingDown className="w-4 h-4" />}
                    </div>
                  </div>

                  {/* Kart Orta: Canlı Fiyat */}
                  <div className="my-2 font-mono">
                    <div className="text-[10px] text-slate-400 mb-0.5">SON FİYAT</div>
                    <div className="text-3xl font-bold tracking-tight text-slate-100">
                      ₺{item.Fiyat}
                    </div>
                  </div>

                  {/* Kart Alt: Hacim ve Yüzdelik Değişim */}
                  <div className="pt-4 border-t border-slate-800/80 mt-3 flex justify-between items-center text-xs font-mono">
                    <div className="flex items-center gap-1.5 text-slate-400 text-[11px]">
                      <BarChart3 className="w-3.5 h-3.5 text-slate-500" />
                      <span>{(parseInt(item.Hacim || "0") / 1000000).toFixed(2)}M</span>
                    </div>

                    <span
                      className={`font-bold px-2 py-0.5 rounded text-[11px] ${
                        artismi
                          ? "bg-emerald-500/10 text-emerald-400"
                          : "bg-rose-500/10 text-rose-400"
                      }`}
                    >
                      {artismi ? "+" : ""}{item.Günlük_Değişim_Yüzde}%
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}