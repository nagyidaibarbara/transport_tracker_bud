# C:\Users\nagyi\transport_tracker\backend\main.py (JAVÍTVA)
from fastapi import FastAPI
from backend.api.v1 import endpoints
# 🛑 JAVÍTÁS: Base a models-ből, engine a core.database-ből
from backend.models.transport_data import Base  # <--- Base ide!
from backend.core.database import engine       # <--- engine ide!
from backend.core.logging import setup_logging
from backend.background_tasks.scheduler import start_scheduler
import logging



# Logolás beállítása
setup_logging()
logger = logging.getLogger(__name__)


# FastAPI alkalmazás létrehozása
app = FastAPI(title="Transport Tracker Backend")

# API routerek hozzáadása
app.include_router(endpoints.router, prefix="/api/v1", tags=["Transport Data"])


@app.on_event("startup")
def startup_event():
    """Esemény, ami az alkalmazás indításakor fut le."""
    logger.info("FastAPI Alkalmazás indítása...")

    # Adatbázis táblák létrehozása (OOP)
    # A táblák csak akkor jönnek létre, ha még nem léteznek
    Base.metadata.create_all(bind=engine)
    logger.info("Adatbázis inicializálva.")

    # Automatizált feladatvégzés elindítása
    start_scheduler()
    logger.info("Háttér ütemező elindítva.")


@app.get("/", include_in_schema=False)
def root():
    return {"message": "Transport Tracker Backend is running. Access /docs for API documentation."}