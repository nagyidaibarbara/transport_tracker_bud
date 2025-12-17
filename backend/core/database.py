
# C:\Users\nagyi\transport_tracker\backend\core\database.py (JAVÍTVA)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# 🛑 JAVÍTÁS: A 'database.py' a 'core' mappában van. A 'config.py' a 'core' mappában van.
# Csak egy pont (.), mert ugyanabban a mappában van a config fájl!
from .config import settings




# Adatbázis motor létrehozása
engine = create_engine(
    settings.DATABASE_URL, connect_args={"check_same_thread": False} # Csak SQLite esetén kell
)

# A SessionLocal osztály egy session készítő, minden kéréshez új session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Függőség injektálás a FastAPI-hoz
def get_db():
    """DB sessiont ad vissza, majd bezárja azt a kérés befejezése után."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()