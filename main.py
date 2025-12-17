# main.py (a transport_tracker/ mappában)
import subprocess
import logging
import time
from backend.core.logging import setup_logging

# A main.py csak a szerver indításáért felel, a scheduler és DB setup a backend/main.py-ban van

if __name__ == "__main__":
    setup_logging()

    print("\n----------------------------------------------------")
    print("🚀 Transport Tracker Rendszer Indítása...")

    # 1. Start FastAPI Backend (Mikroszerviz 1)
    logging.info("FastAPI Backend indítása (http://0.0.0.0:8000)")

    # uvicorn futtatása (a backend/main:app fájlt célozza meg)



    # C:\Users\nagyi\transport_tracker\main.py (JAVÍTVA)
    subprocess.run(
        # Futtassuk Uvicorn-t a shellből, ami beállítja a PATH-ot
        ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"],
        check=True
    )


    # Megjegyzés: A scheduler a backend/main.py startup eventjével indul el.

    print("----------------------------------------------------")
    print("❌ FastAPI leállt. A Streamlit külön terminálban futtatható.")