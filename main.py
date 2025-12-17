import subprocess
import logging
import time
import uvicorn
from backend.core.logging import setup_logging
from backend.main import app  # <--- EZ KELL A RENDERNEK

# Fontos: A Render az "app" változót keresi ebben a fájlban.
# Az importálás révén a Render már látja, de a biztonság kedvéért:
app = app

if __name__ == "__main__":
    setup_logging()

    print("\n----------------------------------------------------")
    print("🚀 Transport Tracker Rendszer Indítása...")

    # 1. Start FastAPI Backend (Mikroszerviz 1)
    logging.info("FastAPI Backend indítása (http://0.0.0.0:8000)")

    # Lokális futtatáskor a te subprocess-es megoldásod marad:
    try:
        subprocess.run(
            ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"],
            check=True
        )
    except KeyboardInterrupt:
        logging.info("Leállítás folyamatban...")

    print("----------------------------------------------------")
    print("❌ FastAPI leállt. A Streamlit külön terminálban futtatható.")