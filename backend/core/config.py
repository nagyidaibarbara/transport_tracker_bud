from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    # A .env fájl betöltése a gyökérkönyvtárból
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    # Adatbázis URL
    DATABASE_URL: str = "sqlite:///./transport.db"

    # Külső API
    BKK_API_URL: str = "https://example-transport-api.com/realtime"
    API_KEY: Optional[str] = None

    LOG_LEVEL: str = "INFO"
    # A Streamlit frontend a Render URL-jét fogja használni
    API_BASE_URL: str = "http://localhost:8000"


settings = Settings()