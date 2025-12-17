📄 Projekt Dokumentáció - Transport Tracker
1. Rendszerarchitektúra
Az alkalmazás mikroszerviz-alapú architektúrát követ, ahol a komponensek lazán kapcsoltak:

Adatbázis: SQLite fájl alapú adatbázis SQLAlchemy ORM-mel kezelve.

Backend: FastAPI keretrendszer, amely biztosítja a REST API végpontokat és az aszinkron háttérfolyamatokat.

Frontend: Streamlit alapú webes felület, amely a Backend API-tól kapott JSON adatokat vizualizálja.

2. Megvalósított Paradigmák
Objektumorientált (OOP): Az adatok modellezése osztályokkal történt (VehiclePosition), a szolgáltatások pedig Service osztályokba (NewsService, DataService) lettek csoportosítva.

Procedurális: A rendszer indítási folyamata és az adatgyűjtési ciklus szekvenciális vezérlése.

Funkcionális: List comprehension és beépített szűrőfüggvények használata az adatok transzformálása során (pl. scraping adatok tisztítása).

3. Technikai specifikáció
Web Scraping: A BeautifulSoup4 könyvtár segítségével a rendszer a bud.hu weboldalról gyűjt aktuális közlekedési híreket.

Adatvalidáció: A Pydantic modellek garantálják, hogy csak valid adatok kerüljenek az API-ból a frontendhez.

Automatizáció: A FastAPI startup_event dekorátora indítja el az asyncio alapú ütemezőt, amely 15 másodpercenként frissíti a járműpozíciókat.

Hibakezelés: Logolás (logging modul) és try-except blokkok biztosítják a robusztus működést hálózati hiba esetén is.

4. Tesztelési jegyzőkönyv
A tesztelés pytest keretrendszerrel történt.

Egységteszt 1: API végpontok elérhetősége.

Egységteszt 2: Web Scraping adatstruktúra ellenőrzése.

Egységteszt 3 (@pytest.mark.parametrize): Statisztikai modul ellenőrzése különböző bemeneti adathalmazokon.