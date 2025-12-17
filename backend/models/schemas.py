from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

class VehiclePositionRead(BaseModel):
    """Pydantic modell a járműpozíciók olvasásához"""
    vehicle_id: str
    latitude: float
    longitude: float
    delay_seconds: int = Field(alias="delay")
    timestamp: datetime

    class Config:
        from_attributes = True
        populate_by_name = True

class StatsRead(BaseModel):
    """Pydantic modell a statisztikákhoz"""
    active_vehicles: int
    avg_delay: float
    max_delay: int

class NewsRead(BaseModel):
    """Pydantic modell a web scraping hírekhez"""
    news: List[str]