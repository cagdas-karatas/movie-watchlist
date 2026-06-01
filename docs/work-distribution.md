# İş Paylaşımı — Movie Watchlist

## Üyeler

- Çağdaş Karataş — Backend, Veritabanı, Test
- Eren Şeremet — UI, Deployment, CI/CD

## Modül Sorumluluğu

| Modül | Sorumlu | Açıklama |
|---|---|---|
| FastAPI endpoint'leri (`src/main.py`) | Çağdaş | 8 REST endpoint, CORS, startup |
| Veritabanı katmanı (`src/database.py`) | Çağdaş | SQLAlchemy engine, session yönetimi |
| ORM modeli (`src/models.py`) | Çağdaş | Movie entity, 9 alan |
| Pydantic şemaları (`src/schemas.py`) | Çağdaş | Request/response modelleri, validator |
| Servis katmanı (`src/services/movie_service.py`) | Çağdaş | CRUD, search, stats iş mantığı |
| Unit testler (`tests/unit/`) | Çağdaş | 23 test, %94 coverage |
| Integration testler (`tests/integration/`) | Çağdaş | 3 test, Testcontainers + PostgreSQL |
| E2E testler (`tests/e2e/`) | Çağdaş | 4 test, Playwright |
| Test altyapısı (`tests/conftest.py`, `factories.py`) | Çağdaş | Fixture'lar, MovieFactory |
| Postman koleksiyonu (`postman/`) | Çağdaş | 5 istek, 10 assertion |
| Streamlit UI (`ui/streamlit_app.py`) | Eren | Film listesi, form, arama |
| Dockerfile (multi-stage) | Eren | Builder + runtime aşamaları |
| docker-compose.yml | Eren | postgres + app + ui servisleri |
| Kubernetes manifestleri (`k8s/`) | Eren | Deployment, Service, ConfigMap, Secret |
| GitHub Actions (`ci.yml`) | Eren | lint → test → build → newman → k8s-validate |
| Final rapor ve belgeler (`docs/`) | Çağdaş + Eren | Birlikte hazırlandı |

## Sunum Sorumluluğu

| Bölüm | Süre | Sorumlu |
|---|---|---|
| Problem & Çözüm, Mimari, API Endpoint'leri | 0 – 5 dk | Çağdaş |
| Test Stratejisi, Test Piramidi | 5 – 8 dk | Çağdaş |
| Docker, Kubernetes, CI/CD Pipeline | 8 – 13 dk | Eren |
| Canlı Demo | 13 – 17 dk | Çağdaş + Eren |
| Sayılar, Öğrendiklerim, Q&A | 17 – 20 dk | Çağdaş + Eren |
