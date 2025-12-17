from sqlalchemy.orm import Session
from backend.models.transport_data import VehiclePosition
from datetime import datetime
import random


class DataService:
    def __init__(self, db: Session):
        self.db = db

    def _generate_mock_flights(self):
        """Saját adatgenerátor a repülőtérhez (ha nincs külső API)."""
        flight_list = [
            {"id": "W62341", "r": "BUD-LTN", "lat": 47.43, "lon": 19.23},
            {"id": "LH1678", "r": "MUC-BUD", "lat": 47.45, "lon": 19.30},
            {"id": "FR8372", "r": "BUD-STN", "lat": 47.40, "lon": 19.15},
            {"id": "OS718", "r": "VIE-BUD", "lat": 47.48, "lon": 19.28}
        ]
        return flight_list

    async def fetch_and_save_data_pipeline(self):
        """
        Ez a függvény valósítja meg az automatizált adatmentést a SAJÁT adatbázisba.
        """
        flights = self._generate_mock_flights()
        count = 0

        for f in flights:
            # Új rekord létrehozása az SQLAlchemy modell alapján
            new_entry = VehiclePosition(
                vehicle_id=f["id"],
                route_id=f["r"],
                latitude=f["lat"] + (random.uniform(-0.01, 0.01)),  # Kis mozgás szimuláció
                longitude=f["lon"] + (random.uniform(-0.01, 0.01)),
                speed=850.0,
                delay_seconds=random.randint(0, 30),
                timestamp=datetime.utcnow()
            )
            self.db.add(new_entry)
            count += 1

        self.db.commit()  # Adatok véglegesítése az adatbázisban
        return count

    def get_latest_positions(self):
        """Lekérdezés a saját adatbázisból."""
        return self.db.query(VehiclePosition).order_by(VehiclePosition.timestamp.desc()).limit(10).all()

    def calculate_delay_stats(self):
        """Statisztika készítése az adatbázis adatai alapján."""
        positions = self.get_latest_positions()
        if not positions:
            return {"active_vehicles": 0, "avg_delay": 0.0, "max_delay": 0}

        delays = [p.delay_seconds for p in positions]
        return {
            "active_vehicles": len(positions),
            "avg_delay": sum(delays) / len(delays),
            "max_delay": max(delays)
        }