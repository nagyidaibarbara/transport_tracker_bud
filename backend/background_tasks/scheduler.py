# backend/background_tasks/scheduler.py (ABSZOLÚT JAVÍTÁS)

import schedule
import time
import threading
import asyncio
import logging

# 🛑 JAVÍTÁS: Abszolút importok a 'backend' csomagra utalva!
from backend.services.data_service import DataService
from backend.core.database import SessionLocal

logger = logging.getLogger(__name__)




def run_data_pipeline():
    """
    A schedule által futtatott belépési pont.
    Ez hívja a DataService aszinkron, procedurális pipeline-ját.
    """
    db = SessionLocal()
    try:
        service = DataService(db)
        # Az asyncio.run() segítségével futtatjuk a Service aszinkron metódusát a szinkron szálról.
        asyncio.run(service.fetch_and_save_data_pipeline())
    except Exception as e:
        logger.error(f"Hiba a scheduled feladatban: {e}")
    finally:
        db.close()


def start_scheduler():
    """Elindítja az ütemezőt egy különálló szálon (threading)."""
    logger.info("Scheduler elindult. Adatgyűjtés 10 másodpercenként.")

    # Automatizált feladat: 10 másodpercenként futtatja a feladatot
    # Ezzel teljesítjük az automatizált feladatvégzés követelményét
    schedule.every(10).seconds.do(run_data_pipeline)

    def run_pending():
        """Folyamatosan ellenőrzi az ütemezett feladatokat."""
        while True:
            schedule.run_pending()
            time.sleep(1)

    # A scheduler egy külön Daemon szálon fut, ami nem blokkolja a FastAPI-t.
    scheduler_thread = threading.Thread(target=run_pending, daemon=True)
    scheduler_thread.name = "TransportSchedulerThread"
    scheduler_thread.start()
    return scheduler_thread