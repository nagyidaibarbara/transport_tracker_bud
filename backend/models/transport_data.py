# backend/models/transport_data.py
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import List

# OOP: Alap entitás osztály
Base = declarative_base()

class VehiclePosition(Base):
    """
    SQLAlchemy Modell: A járműpozíciók tartós tárolása az adatbázisban.
    """
    __tablename__ = "vehicle_positions"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(String, index=True, nullable=False)
    route_id = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    speed = Column(Float, default=0.0)
    delay_seconds = Column(Integer, default=0)
    timestamp = Column(DateTime, default=datetime.utcnow)

# ---------------- Pydantic Sémák ----------------

# Pydantic Alapkonfiguráció
class TransportBase(BaseModel):
    # Streamlit Cloud/Render.com környezeti változók kezelése
    model_config = ConfigDict(from_attributes=True)

# Bemeneti adat validáció (API/Scheduler kimenete)
class VehiclePositionCreate(TransportBase):
    vehicle_id: str
    route_id: str
    latitude: float
    longitude: float
    speed: float = 0.0
    delay_seconds: int = 0
    timestamp: datetime = datetime.utcnow()

# Kimeneti adat (API válasz a frontend számára)
class VehiclePositionRead(VehiclePositionCreate):
    id: int

# Statisztikai kimenet
class StatsRead(TransportBase):
    avg_delay: float
    max_delay: int
    active_vehicles: int