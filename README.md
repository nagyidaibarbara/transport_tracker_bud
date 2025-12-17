# ✈️ BUD Airport Monitor - Backend & Frontend

Ez egy valós idejű repülőtéri járati monitor alkalmazás az Eszterházy Károly Katolikus Egyetem Multi-paradigmás programozási nyelvek gyakorlatára.

## 🌐 Élő elérhetőségek
- **Frontend (Streamlit Cloud):** https://transporttrackerbud-t77wxktibeotuh2uo46eeg.streamlit.app/
- **Backend API (Render - Swagger UI):** https://transport-tracker-bud.onrender.com/docs

*Megjegyzés: Az ingyenes Render.com tárhely miatt az első betöltés (a szerver ébredése) kb. 50-60 másodpercet vehet igénybe.*

## ✨ Megvalósított követelmények
- **Paradigmák:** Procedurális, Funkcionális és Objektumorientált (OOP) szemlélet.
- **Backend:** FastAPI REST API, Pydantic validációval.
- **Adatbázis:** SQLAlchemy ORM (SQLite).
- **Automatizáció:** Háttérben futó aszinkron adatgenerálás és Web Scraping (BeautifulSoup4).
- **Frontend:** Interaktív Streamlit felület térképpel és statisztikákkal.
- **Tesztelés:** Pytest egységtesztek (@pytest.mark.parametrize).

## 🚀 Helyi indítás
1. `pip install -r requirements.txt`
2. `python main.py` (Backend indítása)
3. `streamlit run frontend/app.py` (Frontend indítása)