# backend/api/v1/endpoints.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict
import httpx
import logging

# Abszolút importok a projekt struktúrája szerint
from backend.core.database import get_db
from backend.services.data_service import DataService
from backend.services.news_service import NewsService
# A modellek/sémák importálása (Pydantic)
from backend.models.transport_data import VehiclePositionRead, StatsRead

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/vehicles/latest", response_model=List[VehiclePositionRead], status_code=status.HTTP_200_OK)
def get_latest_positions_endpoint(db: Session = Depends(get_db)):
    """Backend végpont: A legfrissebb járműpozíciók listája (OOP)."""
    try:
        service = DataService(db)
        return service.get_latest_positions()
    except Exception as e:
        logger.error(f"Hiba a pozíciók lekérésekor: {e}")
        raise HTTPException(status_code=500, detail="Hiba a belső szolgáltatásban (DB lekérdezés).")

@router.get("/stats", response_model=StatsRead, status_code=status.HTTP_200_OK)
def get_delay_stats(db: Session = Depends(get_db)):
    """Backend végpont: Statisztikák (FP és OOP elemekkel)."""
    try:
        service = DataService(db)
        return service.calculate_delay_stats()
    except Exception as e:
        logger.error(f"Hiba a statisztikák kiszámításakor: {e}")
        raise HTTPException(status_code=500, detail="Hiba a statisztikai modulban.")

@router.post("/collect_now", status_code=status.HTTP_202_ACCEPTED)
async def trigger_collection(db: Session = Depends(get_db)):
    """
    Kézi trigger: Aszinkron adatgyűjtési pipeline (PP).
    Webes hívást kezdeményez a háttérben.
    """
    service = DataService(db)
    try:
        count = await service.fetch_and_save_data_pipeline()
        return {"message": "Adatgyűjtés sikeresen befejeződött.", "count": count}
    except httpx.HTTPStatusError as e:
        logger.error(f"Külső API hiba: {e}")
        raise HTTPException(status_code=503, detail=f"Külső API hiba: {e.response.status_code}")
    except Exception as e:
        logger.error(f"Hiba az adatgyűjtés során: {e}")
        raise HTTPException(status_code=500, detail=f"Hiba az adatgyűjtés során: {e}")

@router.get("/news", status_code=status.HTTP_200_OK)
def get_latest_news():
    """
    Végpont a web scraping alapú hírek kiszolgálásához.
    Ez teljesíti a 'külső adatforrás' és 'BeautifulSoup' követelményt.
    """
    try:
        news = NewsService.fetch_transport_news()
        return {"news": news}
    except Exception as e:
        logger.error(f"Hiba a hírek lekérésekor: {e}")
        return {"news": ["Nem sikerült friss híreket betölteni."]}