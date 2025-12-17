import streamlit as st
import pandas as pd
import requests
import time
import os
from datetime import datetime
from dotenv import load_dotenv

# 1. Konfiguráció betöltése
load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000/api/v1")

st.set_page_config(layout="wide", page_title="BUD Reptér Monitor")


# 2. Adatlekérő függvény
def fetch_data(endpoint: str):
    """Kommunikáció a Backenddel (Saját API hívás lánc)"""
    try:
        response = requests.get(f"{BACKEND_URL}{endpoint}", timeout=3)
        if response.status_code == 200:
            return response.json()
    except Exception:
        return None
    return None


# --- UI Felület ---
st.title("✈️ Budapest Airport - Élő Járati Monitor")

# Oldalsáv statikus részei
st.sidebar.header("📊 Napi Statisztika")
stats_placeholder = st.sidebar.empty()

st.sidebar.markdown("---")
st.sidebar.subheader("📢 Reptéri Közlemények")
news_placeholder = st.sidebar.empty()

# Főoldali tartalom helye
main_placeholder = st.empty()

# 3. Dinamikus frissítési ciklus (Automatizáció)
while True:
    # --- A: Statisztikák lekérése és megjelenítése ---
    stats = fetch_data("/stats")
    with stats_placeholder.container():
        if stats:
            st.metric("Aktív Járatok", stats.get('active_vehicles', 0))
            st.metric("Átlagos Késés", f"{stats.get('avg_delay', 0.0):.1f} perc")
        else:
            st.warning("Adatbázis üres...")

    # --- B: Hírek lekérése (Web Scraping eredménye) ---
    news_data = fetch_data("/news")
    with news_placeholder.container():
        if news_data and "news" in news_data:
            for item in news_data["news"]:
                st.info(item)
        else:
            st.write("Hírek betöltése...")

    # --- C: Járatadatok és Térkép (Vizualizáció) ---
    data = fetch_data("/vehicles/latest")
    with main_placeholder.container():
        if data and isinstance(data, list) and len(data) > 0:
            df = pd.DataFrame(data)

            # Térkép megjelenítése (Pydantic modellekből jövő lat/lon alapján)
            st.subheader("Légiforgalmi Helyzetkép (BUD körzet)")
            # Biztosítjuk, hogy a térkép az oszlopneveket felismerje
            st.map(df[['latitude', 'longitude']], zoom=10)

            # Táblázatos nézet (Adatbázis tartalom vizualizálása)
            st.subheader("Aktuális Menetrend")
            # Megjelenítendő oszlopok szűrése és átnevezése
            display_cols = {
                'vehicle_id': 'Járat ID',
                'route_id': 'Útvonal',
                'delay_seconds': 'Késés (perc)'
            }
            # Csak azokat az oszlopokat használjuk, amik léteznek a DF-ben
            existing_cols = [c for c in display_cols.keys() if c in df.columns]
            st.dataframe(df[existing_cols].rename(columns=display_cols), use_container_width=True)

            st.caption(f"Utolsó sikeres lekérdezés a saját adatbázisból: {datetime.now().strftime('%H:%M:%S')}")
        else:
            st.warning("⚠️ Nincs aktív járat az adatbázisban. Kérlek, indítsd el az adatgyűjtést a Backenden!")
            # Ha teljesen üres, mutatunk egy gombot, amivel megpöccinthető a backend
            if st.button("Adatgyűjtés azonnali indítása"):
                requests.post(f"{BACKEND_URL}/collect_now")
                st.rerun()

    # Frissítési gyakoriság: 5 másodperc (beadandó követelmény az automatizációra)
    time.sleep(5)