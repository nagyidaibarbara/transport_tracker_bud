# tests/test_service.py
import pytest
from backend.services.data_service import DataService
from backend.models.transport_data import VehiclePositionCreate
from datetime import datetime
from unittest.mock import MagicMock
import statistics
import asyncio
import httpx


# Mock DB Session létrehozása a teszteléshez
@pytest.fixture
def mock_db_session():
    return MagicMock()


@pytest.fixture
def data_service(mock_db_session):
    return DataService(db=mock_db_session)


# 1. Teszt: Parametrizált teszt a funkcionális részre (FP logika)
@pytest.mark.parametrize("input_delays, expected_max, expected_avg", [
    ([10, 20, 5, 15], 20, 12.5),  # Alap eset
    ([100, 10, 50, 0, -5], 100, 53.33),  # Negatív értékek szűrése (FP)
    ([], 0, 0.0),  # Üres eset
])
def test_calculate_delay_stats_fp(input_delays, expected_max, expected_avg, data_service):
    """
    Teszteli a késések aggregációját (FP jellegű logika).
    A @pytest.mark.parametrize dekorátor használatával.
    """

    # A mock beállítása: A lekérdezés eredménye tuple-ök listája (ahogy az SQLAlchemy visszaadja)
    mock_delays = [(d,) for d in input_delays]

    # A mock DB-t úgy állítjuk be, hogy visszaadja a tesztadatokat
    data_service.db.query().filter().all.return_value = mock_delays
    data_service.db.query().filter().distinct().count.return_value = 5  # Mock aktív járművek száma

    stats = data_service.calculate_delay_stats()

    # A 0-t és a negatívokat a számításnak figyelmen kívül kell hagynia
    positive_delays = [d for d in input_delays if d > 0]

    if positive_delays:
        assert stats["max_delay"] == max(positive_delays)
        # Az átlagot a Service-ben 2 tizedesre kerekítjük
        assert stats["avg_delay"] == round(statistics.mean(positive_delays), 2)
    else:
        assert stats["avg_delay"] == 0.0
        assert stats["max_delay"] == 0


# 2. Teszt: OOP metódus tesztelése (DB mentés)
def test_save_new_positions_oop(data_service, mock_db_session):
    """Teszteli az OOP mentési metódust és az SQLAlchemy interakciót."""

    mock_positions = [
        VehiclePositionCreate(vehicle_id="V001", route_id="101", latitude=47.0, longitude=19.0),
    ]

    data_service.save_new_positions(mock_positions)

    # Ellenőrizzük, hogy az add_all és a commit hívva lett-e az OOP osztályon
    mock_db_session.add_all.assert_called_once()
    mock_db_session.commit.assert_called_once()


# 3. Teszt: API lánc/Aszinkron adatgyűjtés tesztelése (PP logika)
@pytest.mark.asyncio
async def test_fetch_and_save_data_pipeline_pp(data_service, mocker):
    """
    Teszteli a Procedurális pipeline futását.
    Aszinkron teszt, amely mockolja a külső API hívást.
    """

    # Mockoljuk a külső API-t (Valós Adat) a mock_realtime_data függvénnyel
    mocker.patch.object(data_service, '_fetch_external_api_data', return_value=data_service._mock_realtime_data())

    # Mockoljuk a mentési lépést
    mocker.patch.object(data_service, 'save_new_positions')

    # Futtatjuk a teljes PP pipeline-t
    count = await data_service.fetch_and_save_data_pipeline()

    # Ellenőrizzük, hogy a három fő procedúra lépés lefutott:
    data_service._fetch_external_api_data.assert_called_once()  # 1. Lépés (async)
    data_service.save_new_positions.assert_called_once()  # 3. Lépés (OOP)

    # Az mock adatokból 2 elem jön vissza
    assert count == 2