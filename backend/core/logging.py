import logging
from .config import settings

# A logging modul beállítása
def setup_logging():
    logging.basicConfig(
        level=settings.LOG_LEVEL,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("app.log", mode='a'), # Fájlba írás
            logging.StreamHandler()                    # Konzolra írás
        ]
    )
    logging.info("Logolás beállítva.")