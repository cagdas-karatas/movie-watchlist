# Movie Watchlist — Bulut Mimarilerinde Test Mühendisliği Dönem Projesi

> **Bu dosya Claude Code agent için yazılmıştır.** Aşağıdaki fazları **sırayla** uygula. Her fazın sonundaki **Kabul Kriteri** sağlanmadan bir sonraki faza geçme. Kullanıcının manuel yapması gereken adımlar **🧑 KULLANICI AKSİYONU** etiketiyle işaretlenmiştir — bu adımlara geldiğinde dur, kullanıcıdan onay bekle, sonra devam et.

## Proje Özeti

- **Konu:** Movie Watchlist (film izleme listesi servisi)
- **Dil/Framework:** Python 3.11 + FastAPI
- **DB:** SQLite (lokal dev) + PostgreSQL (integration test & prod)
- **UI:** Streamlit (sadece E2E test için basit arayüz)
- **Atlanan rubric kalemleri:** Monitoring (Prometheus/Grafana), Performans (k6/Locust), AWS/LocalStack
- **Hedef puan:** 85/100

## Genel Kurallar (Agent için)

1. Her faz sonunda kullanıcıya **kısa bir özet** ver: ne yapıldı, hangi dosyalar oluştu/değişti.
2. **Commit at** her fazın sonunda. Commit mesajları anlamlı olsun (örn: `feat: add movie service layer`, `test: add integration tests with testcontainers`).
3. **Asla** atlanmış olarak işaretlenen kalemlere (monitoring, performans, LocalStack/AWS, S3, boto3) referans verme. `requirements.txt`'e `prometheus-client`, `boto3`, `locust` gibi paketler ekleme.
4. Kod yazarken **type hints** kullan, **docstring** ekle. Sunumda savunulabilirlik için kod okunabilir olmalı.
5. Hata aldığında kullanıcıya açıkla, çözüm öner, gerekirse onay iste.
6. Türkçe ve İngilizce karışık konuşabilirsin ama kod & commit mesajları İngilizce.

---

# 🧑 KULLANICI AKSİYONU — Faz 0 Öncesi Hazırlık

Agent'a başlamadan önce kullanıcının **manuel** yapması gerekenler:

1. **GitHub'da yeni public repo aç:** `movie-watchlist` adıyla
2. **Repo'yu lokale klonla:** `git clone <repo-url> && cd movie-watchlist`
3. **Eğitmeni collaborator olarak ekle:** GitHub repo settings → Collaborators → `busraayaksiz` (veya şartnamede verilen GitHub username) — *Şartnamede tam username yazılı değil, kullanıcı eğitmene mail atıp doğrulamalı.*
4. **Python 3.11 kurulu mu kontrol et:** `python3.11 --version`. Yoksa kur.
5. **Docker Desktop kurulu ve çalışıyor mu:** `docker --version && docker ps`. Yoksa [docker.com](https://www.docker.com/products/docker-desktop/)'dan indir.
6. **Minikube kurulu mu:** `minikube version`. Yoksa [minikube.sigs.k8s.io](https://minikube.sigs.k8s.io/docs/start/)'dan indir.
7. **kubectl kurulu mu:** `kubectl version --client`. Yoksa kur.
8. **Postman Desktop kurulu mu** (Postman koleksiyonu için). Yoksa [postman.com](https://www.postman.com/downloads/)'dan indir.
9. **Node.js kurulu mu** (Newman için): `node --version`. Yoksa [nodejs.org](https://nodejs.org/)'dan LTS indir.
10. **Newman CLI kur:** `npm install -g newman`
11. **Google Form'u doldur** (proje konu seçimi) — şartnamedeki link
12. **Google Calendar booking yap** — sunum slotu için

Tüm bunlar tamamlandığında agent'a "başla" de.

---

# Faz 0 · Repo İskeleti ve Bağımlılıklar (15 dk)

## Hedef
Klasör yapısını ve temel config dosyalarını oluştur. Henüz kod yazma.

## Adımlar

### 0.1 — Klasör yapısını oluştur
```
movie-watchlist/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   └── services/
│       ├── __init__.py
│       └── movie_service.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── factories.py
│   ├── unit/
│   │   └── __init__.py
│   ├── integration/
│   │   └── __init__.py
│   └── e2e/
│       └── __init__.py
├── ui/
│   └── streamlit_app.py
├── postman/
├── k8s/
├── monitoring/    # boş bırak (rubric'te var ama atlıyoruz)
├── perf/          # boş bırak
├── .github/
│   └── workflows/
├── docs/
├── .gitignore
├── .dockerignore
├── README.md
├── LICENSE
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── Dockerfile
└── docker-compose.yml
```

### 0.2 — `.gitignore` oluştur
Python, venv, pytest cache, .env, __pycache__, *.db, .coverage, htmlcov/, .pytest_cache, node_modules, .DS_Store içermeli.

### 0.3 — `.dockerignore` oluştur
.git, tests/, docs/, *.md, .github/, .venv/, __pycache__, .pytest_cache, .coverage, ui/ içermeli.

### 0.4 — `requirements.txt` (runtime dependencies)
```
fastapi==0.115.0
uvicorn[standard]==0.32.0
sqlalchemy==2.0.35
pydantic==2.9.2
psycopg2-binary==2.9.10
python-dotenv==1.0.1
```

### 0.5 — `requirements-dev.txt` (dev/test dependencies)
```
-r requirements.txt
pytest==8.3.3
pytest-cov==5.0.0
pytest-asyncio==0.24.0
httpx==0.27.2
factory-boy==3.3.1
faker==30.3.0
testcontainers[postgres]==4.8.2
playwright==1.47.0
streamlit==1.39.0
requests==2.32.3
ruff==0.6.9
```

### 0.6 — `LICENSE` oluştur
MIT lisansı, sahibi: kullanıcının adı (kullanıcıya sor).

### 0.7 — Virtual environment kur
```bash
python3.11 -m venv .venv
source .venv/bin/activate  # (Windows: .venv\Scripts\activate)
pip install --upgrade pip
pip install -r requirements-dev.txt
playwright install chromium
```

### 0.8 — İlk commit
```bash
git add .
git commit -m "chore: initial project skeleton and dependencies"
git push origin main
```

## ✅ Kabul Kriteri
- `tree -L 2` veya `ls -R` ile yukardaki klasör yapısı görünüyor
- `pip list` çıktısında fastapi, pytest, streamlit görünüyor
- GitHub'da ilk commit görünüyor

## 🧑 KULLANICI AKSİYONU — Faz 0 Sonu
Kullanıcıya: "İlk commit pushlandı, GitHub'da gör. Devam edebilir miyim?" diye sor.

---

# Faz 1 · Veritabanı Modeli ve Bağlantı (30 dk)

## Hedef
SQLAlchemy modeli, Pydantic şemaları ve DB session yönetimi.

## Adımlar

### 1.1 — `src/database.py`
- `DATABASE_URL` ortam değişkeninden oku, yoksa default `sqlite:///./movies.db`
- SQLAlchemy `create_engine` (SQLite için `connect_args={"check_same_thread": False}`)
- `SessionLocal` ve `Base` tanımla
- `get_db()` generator (FastAPI dependency)
- `init_db()` fonksiyonu — tabloları oluştur

### 1.2 — `src/models.py`
SQLAlchemy `Movie` modeli:

| Kolon | Tip | Notlar |
|---|---|---|
| `id` | Integer | primary_key, autoincrement |
| `title` | String(200) | nullable=False, index=True |
| `director` | String(100) | nullable=True |
| `year` | Integer | nullable=True |
| `genre` | String(50) | nullable=True, index=True |
| `watched` | Boolean | default=False, nullable=False |
| `rating` | Integer | nullable=True (1-10 arası, app-level validate) |
| `added_at` | DateTime | default=datetime.utcnow |
| `watched_at` | DateTime | nullable=True |

### 1.3 — `src/schemas.py`
Pydantic v2 modelleri:
- `MovieBase` — title, director, year, genre (ortak alanlar)
- `MovieCreate(MovieBase)` — yaratırken
- `MovieUpdate` — tüm alanlar Optional (PATCH için), `watched` ve `rating` dahil
- `MovieResponse(MovieBase)` — id, watched, rating, added_at, watched_at; `model_config = ConfigDict(from_attributes=True)`
- `StatsResponse` — total: int, watched_count: int, unwatched_count: int, avg_rating: float | None

`rating` için validator: 1-10 arası olmalı (None hariç).

### 1.4 — Manuel test
Agent şunu çalıştırıp doğrulasın:
```bash
python -c "from src.database import init_db; init_db(); print('DB created')"
ls -la movies.db
```

## ✅ Kabul Kriteri
- `movies.db` dosyası oluştu
- Import hataları yok: `python -c "from src.models import Movie; from src.schemas import MovieCreate"`

### 1.5 — Commit
```bash
git add src/
git commit -m "feat: add movie model, schemas and database setup"
```

---

# Faz 2 · Service Katmanı (30 dk)

## Hedef
İş mantığını endpoint'lerden ayır — bu coverage'ı %70'e çıkarmanın anahtarı.

## Adımlar

### 2.1 — `src/services/movie_service.py`
Aşağıdaki fonksiyonları yaz, hepsi `db: Session` parametresi alır:

```python
def create_movie(db: Session, movie_data: MovieCreate) -> Movie:
    """Yeni film oluştur, DB'ye kaydet, dön."""

def get_movies(
    db: Session,
    watched: bool | None = None,
    skip: int = 0,
    limit: int = 100
) -> list[Movie]:
    """Filmleri listele. watched filter optional."""

def get_movie_by_id(db: Session, movie_id: int) -> Movie | None:
    """Tek film getir, yoksa None."""

def update_movie(
    db: Session,
    movie_id: int,
    update_data: MovieUpdate
) -> Movie | None:
    """Film güncelle. update_data.watched True yapılırsa watched_at=utcnow set et."""

def delete_movie(db: Session, movie_id: int) -> bool:
    """Sil. Bulunduysa True, yoksa False."""

def search_movies(db: Session, query: str) -> list[Movie]:
    """title VEYA director ILIKE %query%. SQLite için lower() trick'i kullan."""

def get_stats(db: Session) -> dict:
    """
    {
        'total': int,
        'watched_count': int,
        'unwatched_count': int,
        'avg_rating': float | None  # sadece izlenen + rating'i olan filmlerden
    }
    """
```

### 2.2 — Önemli kurallar
- Hiçbir service fonksiyonu HTTPException fırlatmasın — None döndür, endpoint katmanı handle etsin
- `update_movie` içinde `model_dump(exclude_unset=True)` ile sadece gelen alanları güncelle
- Update edilen `Movie`'yi commit + refresh et

## ✅ Kabul Kriteri
- `python -c "from src.services.movie_service import create_movie, get_movies, get_stats; print('OK')"` hatasız çalışır

### 2.3 — Commit
```bash
git commit -am "feat: add movie service layer with CRUD and stats"
```

---

# Faz 3 · FastAPI Endpoint'leri (30 dk)

## Hedef
7 REST endpoint + 1 health check.

## Adımlar

### 3.1 — `src/main.py`

```python
app = FastAPI(title="Movie Watchlist API", version="1.0.0")

# Startup'ta init_db çağır
@app.on_event("startup")
def startup():
    init_db()

# CORS middleware ekle (Streamlit'in çağırabilmesi için)
# allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
```

### 3.2 — Endpoint'ler

| Method | Path | Request Body | Response | Hata Durumları |
|---|---|---|---|---|
| GET | `/health` | - | `{"status": "ok"}` | - |
| POST | `/movies` | `MovieCreate` | `MovieResponse` (201) | 422 (validation) |
| GET | `/movies` | - (query: `watched`, `skip`, `limit`) | `list[MovieResponse]` | - |
| GET | `/movies/search` | (query: `q` zorunlu) | `list[MovieResponse]` | 422 q boşsa |
| GET | `/movies/{movie_id}` | - | `MovieResponse` | 404 |
| PATCH | `/movies/{movie_id}` | `MovieUpdate` | `MovieResponse` | 404 |
| DELETE | `/movies/{movie_id}` | - | 204 No Content | 404 |
| GET | `/stats` | - | `StatsResponse` | - |

**ÖNEMLİ:** `/movies/search` endpoint'i `/movies/{movie_id}` endpoint'inden **ÖNCE** tanımlanmalı, yoksa FastAPI "search"i ID olarak algılar.

### 3.3 — Manuel test
```bash
uvicorn src.main:app --reload
```
Tarayıcıda `http://localhost:8000/docs` aç, agent manuel olarak:
1. POST /movies ile bir film ekle (örn: Inception, Nolan, 2010, Sci-Fi)
2. GET /movies ile listele, döndüğünü doğrula
3. PATCH /movies/1 ile watched=true yap
4. GET /stats ile sayıların güncellendiğini gör

## ✅ Kabul Kriteri
- `http://localhost:8000/docs` açılıyor, 8 endpoint görünüyor
- Manuel testler başarılı

### 3.4 — Commit
```bash
git commit -am "feat: add FastAPI endpoints for movies CRUD"
```

## 🧑 KULLANICI AKSİYONU — Faz 3 Sonu
Kullanıcıya: "Backend hazır, `/docs` adresinden test edebilirsin. Şimdi testlere geçiyorum."

---

# Faz 4 · Unit Testler + Factory (45 dk)

## Hedef
≥%70 coverage, anlamlı testler.

## Adımlar

### 4.1 — `tests/conftest.py`
- `db_session` fixture: in-memory SQLite (`sqlite:///:memory:`), her testte yeni session
- `client` fixture: FastAPI TestClient, `get_db` dependency override
- `MovieFactory` import et, session'a bind et

### 4.2 — `tests/factories.py`
```python
class MovieFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Movie
        sqlalchemy_session_persistence = "commit"

    title = factory.Faker('sentence', nb_words=3)
    director = factory.Faker('name')
    year = factory.Faker('random_int', min=1950, max=2024)
    genre = factory.Faker('random_element',
                          elements=['Action', 'Drama', 'Comedy', 'Sci-Fi', 'Horror'])
    watched = False
    rating = None
```

### 4.3 — `tests/unit/test_movie_service.py`
En az **10 test** yaz:

1. `test_create_movie_success` — title, director ile yarat, ID atandığını doğrula
2. `test_get_movie_by_id_found`
3. `test_get_movie_by_id_not_found_returns_none`
4. `test_get_movies_empty_list`
5. `test_get_movies_filter_by_watched` — 3 film yarat (2 watched, 1 değil), watched=True ile 2 dön
6. `test_get_movies_pagination` — 5 film yarat, skip=2 limit=2 ile 2 dön
7. `test_update_movie_sets_watched_at` — watched=True yapıldığında watched_at None olmayacak
8. `test_update_movie_partial_only_changes_given_fields` — sadece rating gönder, title değişmesin
9. `test_delete_movie_returns_true_when_exists`
10. `test_delete_movie_returns_false_when_not_exists`
11. `test_search_movies_by_title`
12. `test_search_movies_by_director`
13. `test_get_stats_empty_db` — total=0, avg=None
14. `test_get_stats_with_movies` — 4 film (2 watched ratings 8,10), avg=9.0

### 4.4 — `tests/unit/test_endpoints.py`
En az **8 test** yaz:

1. `test_health_endpoint`
2. `test_create_movie_endpoint_returns_201`
3. `test_create_movie_endpoint_invalid_data_returns_422`
4. `test_list_movies_endpoint`
5. `test_get_movie_not_found_returns_404`
6. `test_patch_movie_endpoint`
7. `test_delete_movie_returns_204`
8. `test_search_endpoint`
9. `test_stats_endpoint`

### 4.5 — `pyproject.toml` — pytest & coverage config
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
addopts = "-v --tb=short"

[tool.coverage.run]
source = ["src"]
omit = [
    "src/__init__.py",
    "src/*/  __init__.py",
    "tests/*",
    "ui/*",
]

[tool.coverage.report]
fail_under = 70
show_missing = true
skip_covered = false
```

### 4.6 — Testleri çalıştır
```bash
pytest --cov=src --cov-report=term-missing
```

Coverage <%70 ise hangi satırların atlandığını gör, eksik testleri yaz.

## ✅ Kabul Kriteri
- Tüm testler PASS
- Coverage ≥%70
- `pytest --cov=src --cov-fail-under=70` exit code 0

### 4.7 — Commit
```bash
git commit -am "test: add unit tests for service layer and endpoints"
```

---

# Faz 5 · Integration Testler (Testcontainers + PostgreSQL) (30 dk)

## Hedef
3 integration test, gerçek PostgreSQL'e karşı.

## 🧑 KULLANICI AKSİYONU
Docker Desktop'ın **çalıştığından emin ol** (testcontainers Docker üzerinden PostgreSQL container'ı başlatacak).

## Adımlar

### 5.1 — `tests/integration/conftest.py`
- `postgres_container` fixture (scope="session"): `PostgresContainer("postgres:16")`
- `pg_engine` fixture: container'ın connection URL'inden engine oluştur
- `pg_session` fixture: her testte yeni session, sonunda rollback

### 5.2 — `tests/integration/test_postgres_integration.py`

1. **`test_create_and_retrieve_movie_postgres`** — film yarat, DB'ye yazıldığını query ile doğrula
2. **`test_filter_movies_by_watched_postgres`** — 5 film insert (3 watched), filter ile 3 dönüyor mu
3. **`test_update_persists_to_db_postgres`** — update et, yeni session aç, değişiklik orada mı

### 5.3 — Çalıştır
```bash
pytest tests/integration/ -v
```
İlk çalıştırmada postgres:16 image'ı indirilecek (1-2 dk).

## ✅ Kabul Kriteri
- 3 integration test PASS
- Docker'da test sırasında geçici postgres container'ı görünüyor

### 5.4 — Commit
```bash
git commit -am "test: add integration tests with testcontainers postgres"
```

---

# Faz 6 · Postman Koleksiyonu (15 dk)

## 🧑 KULLANICI AKSİYONU
Postman Desktop'ı aç. Aşağıdaki adımları kullanıcı manuel yapacak çünkü Postman UI'ı agent tarafından kontrol edilemez. Agent kullanıcıya talimatları net versin:

## Adımlar

### 6.1 — Yeni koleksiyon
1. Postman → New → Collection → "Movie Watchlist API"
2. Variables sekmesi → `base_url` = `http://localhost:8000`, `movie_id` = (boş)

### 6.2 — 5 istek ekle

**1. Health Check**
- GET `{{base_url}}/health`
- Tests sekmesi:
```javascript
pm.test("status 200", () => pm.response.to.have.status(200));
pm.test("status is ok", () => pm.expect(pm.response.json().status).to.eql("ok"));
```

**2. Create Movie**
- POST `{{base_url}}/movies`
- Body (raw JSON):
```json
{
  "title": "The Matrix",
  "director": "Wachowski",
  "year": 1999,
  "genre": "Sci-Fi"
}
```
- Tests:
```javascript
pm.test("status 201", () => pm.response.to.have.status(201));
const json = pm.response.json();
pm.collectionVariables.set("movie_id", json.id);
pm.test("has id", () => pm.expect(json.id).to.be.a('number'));
```

**3. List Movies**
- GET `{{base_url}}/movies`
- Tests:
```javascript
pm.test("status 200", () => pm.response.to.have.status(200));
pm.test("is array", () => pm.expect(pm.response.json()).to.be.an('array'));
```

**4. Mark as Watched**
- PATCH `{{base_url}}/movies/{{movie_id}}`
- Body:
```json
{ "watched": true, "rating": 9 }
```
- Tests:
```javascript
pm.test("status 200", () => pm.response.to.have.status(200));
pm.test("is watched", () => pm.expect(pm.response.json().watched).to.eql(true));
```

**5. Stats**
- GET `{{base_url}}/stats`
- Tests:
```javascript
pm.test("status 200", () => pm.response.to.have.status(200));
pm.test("has total", () => pm.expect(pm.response.json()).to.have.property('total'));
```

### 6.3 — Export
Koleksiyon → ... → Export → Collection v2.1 → kaydet → `postman/collection.json`

### 6.4 — Newman ile lokal test
```bash
# Önce backend'i ayrı terminalde başlat
uvicorn src.main:app

# Yeni terminalde
newman run postman/collection.json
```

## ✅ Kabul Kriteri
- `postman/collection.json` repoda var
- `newman run postman/collection.json` 5 istek de PASS

### 6.5 — Commit
```bash
git add postman/
git commit -m "test: add postman collection with newman tests"
```

---

# Faz 7 · Streamlit UI (30 dk)

## Hedef
E2E testlerin tutunabileceği basit ama fonksiyonel arayüz.

## Adımlar

### 7.1 — `ui/streamlit_app.py`

Özellikler:
- **Üstte başlık** + 3 metric (Toplam, İzlenen, İzlenmemiş)
- **Sidebar — "Yeni Film Ekle" formu**:
  - `st.form(key="add_movie_form")` içinde
  - title (text_input, key="input_title")
  - director (text_input, key="input_director")
  - year (number_input, key="input_year", min=1900, max=2030)
  - genre (selectbox, key="input_genre", options=["Action","Drama","Comedy","Sci-Fi","Horror"])
  - submit button (key="submit_add", label="Ekle")
- **Arama kutusu** (text_input, key="search_box")
- **Film listesi** (DataFrame veya kolonlu layout):
  - Her satır: title, director, year, genre, watched checkbox, rating, butonlar
  - "İzlendi" butonu (key=f"watch_{movie_id}")
  - "Sil" butonu (key=f"delete_{movie_id}")

### 7.2 — API URL
```python
import os
API_URL = os.getenv("API_URL", "http://localhost:8000")
```

### 7.3 — Test selectorları için
- Tüm butonlara `key` ver (Playwright `get_by_role("button", name="Ekle")` ile bulacak)
- Form ve inputlara `key` ver
- Liste container'ına unique bir element ekle (örn: `st.markdown('<div id="movie-list"></div>', unsafe_allow_html=True)`)

### 7.4 — Manuel test
```bash
# Terminal 1
uvicorn src.main:app

# Terminal 2
streamlit run ui/streamlit_app.py
```
Tarayıcı `http://localhost:8501` açılacak.

## ✅ Kabul Kriteri
- Streamlit açılıyor, film ekleme/silme/işaretleme çalışıyor
- API hatası alınmıyor

### 7.5 — Commit
```bash
git add ui/
git commit -m "feat: add streamlit UI for movie watchlist"
```

---

# Faz 8 · Docker (Multi-stage + Compose) (30 dk)

## Hedef
Multi-stage Dockerfile + docker-compose.yml (app + postgres + ui).

## Adımlar

### 8.1 — `Dockerfile`
```dockerfile
# ===== Build stage =====
FROM python:3.11-slim AS builder

WORKDIR /build
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# ===== Runtime stage =====
FROM python:3.11-slim AS runtime

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY src/ ./src/

ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 8.2 — `docker-compose.yml`
```yaml
version: '3.9'

services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: movies
      POSTGRES_USER: movieuser
      POSTGRES_PASSWORD: moviepass
    ports:
      - "5432:5432"
    volumes:
      - pg_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U movieuser -d movies"]
      interval: 5s
      retries: 5

  app:
    build: .
    environment:
      DATABASE_URL: postgresql+psycopg2://movieuser:moviepass@postgres:5432/movies
    ports:
      - "8000:8000"
    depends_on:
      postgres:
        condition: service_healthy

  ui:
    image: python:3.11-slim
    working_dir: /app
    volumes:
      - ./ui:/app/ui
      - ./requirements-dev.txt:/app/requirements-dev.txt
    environment:
      API_URL: http://app:8000
    command: >
      bash -c "pip install streamlit requests &&
               streamlit run ui/streamlit_app.py --server.address 0.0.0.0"
    ports:
      - "8501:8501"
    depends_on:
      - app

volumes:
  pg_data:
```

### 8.3 — Build & run
```bash
docker compose build
docker compose up -d
docker compose ps    # üçü de Up olmalı
curl http://localhost:8000/health
```

Image boyutunu kontrol et:
```bash
docker images movie-watchlist
```
~150MB altında olmalı.

### 8.4 — Stop
```bash
docker compose down
```

## ✅ Kabul Kriteri
- `docker compose up` ile 3 servis de ayağa kalkıyor
- `curl localhost:8000/health` 200 dönüyor
- `localhost:8501` Streamlit görünüyor

### 8.5 — Commit
```bash
git add Dockerfile docker-compose.yml .dockerignore
git commit -m "feat: add multi-stage dockerfile and docker-compose"
```

---

# Faz 9 · Kubernetes (Minikube) (45 dk)

## 🧑 KULLANICI AKSİYONU — Minikube başlat
Kullanıcıya talimat ver:
```bash
minikube start --driver=docker --memory=4096 --cpus=2
minikube status
```
Bu komutları kullanıcı çalıştırsın, çıktıyı paylaşsın.

## Adımlar

### 9.1 — Image'ı Minikube'e yükle
```bash
eval $(minikube docker-env)   # Windows: minikube docker-env | Invoke-Expression
docker build -t movie-watchlist:latest .
docker images | grep movie-watchlist
```

### 9.2 — `k8s/configmap.yaml`
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: movie-watchlist-config
data:
  APP_ENV: "production"
  LOG_LEVEL: "info"
---
apiVersion: v1
kind: Secret
metadata:
  name: movie-watchlist-secret
type: Opaque
stringData:
  DATABASE_URL: "postgresql+psycopg2://movieuser:moviepass@postgres:5432/movies"
```

### 9.3 — `k8s/postgres.yaml`
Basit bir PostgreSQL Deployment + Service (production'da uygun değil ama demo için yeterli).
- Deployment: postgres:16-alpine, env (DB/USER/PASS), emptyDir volume
- Service: ClusterIP, port 5432, name "postgres"

### 9.4 — `k8s/deployment.yaml`
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: movie-watchlist
  labels:
    app: movie-watchlist
spec:
  replicas: 2
  selector:
    matchLabels:
      app: movie-watchlist
  template:
    metadata:
      labels:
        app: movie-watchlist
    spec:
      containers:
      - name: app
        image: movie-watchlist:latest
        imagePullPolicy: Never   # Minikube local image
        ports:
        - containerPort: 8000
        envFrom:
        - configMapRef:
            name: movie-watchlist-config
        - secretRef:
            name: movie-watchlist-secret
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "500m"
```

### 9.5 — `k8s/service.yaml`
```yaml
apiVersion: v1
kind: Service
metadata:
  name: movie-watchlist
spec:
  type: NodePort
  selector:
    app: movie-watchlist
  ports:
  - port: 80
    targetPort: 8000
    nodePort: 30080
```

### 9.6 — Deploy et
```bash
kubectl apply -f k8s/
kubectl get pods -w   # tüm pod'lar Running olana kadar bekle
kubectl get svc
minikube service movie-watchlist --url
```
Çıkan URL'ye `/docs` ekleyip aç.

### 9.7 — Troubleshooting
- Pod CrashLoopBackOff → `kubectl logs <pod-name>`
- Image not found → `eval $(minikube docker-env)` yapmayı unutmuş olabilirsin
- DB connection error → postgres pod'unun Running olduğundan emin ol

## ✅ Kabul Kriteri
- `kubectl get pods` → app (2 replica) + postgres Running
- `minikube service movie-watchlist --url` ile alınan URL'den `/docs` açılıyor

### 9.8 — Commit
```bash
git add k8s/
git commit -m "feat: add kubernetes manifests for minikube deployment"
```

---

# Faz 10 · E2E Testler (Playwright) (45 dk)

## Hedef
Streamlit UI üzerinden 4 senaryo.

## Adımlar

### 10.1 — `tests/e2e/conftest.py`
- `browser` fixture (scope="session"): playwright sync_api ile chromium launch
- `page` fixture: yeni context + page, her testte temiz
- Test başlamadan önce backend + streamlit'in çalıştığını varsay (CI'da bunu pipeline başlatacak)

### 10.2 — `tests/e2e/test_user_flows.py`

**`STREAMLIT_URL = os.getenv("STREAMLIT_URL", "http://localhost:8501")`**

1. **`test_add_movie_appears_in_list`**
   - Sayfayı aç
   - Sidebar'da title input'a "Test Movie E2E" yaz
   - director "Test Director" yaz
   - year 2023
   - Ekle butonuna tıkla
   - Ana ekranda "Test Movie E2E" text'i görünüyor mu

2. **`test_mark_movie_as_watched_updates_stats`**
   - Önce bir film ekle
   - "İzlendi" butonuna tıkla
   - Stats bölümünde "İzlenen: 1" görünüyor mu

3. **`test_search_filters_movies`**
   - 2 film ekle (farklı title'larla)
   - Arama kutusuna birinin title'ını yaz
   - Sadece o film görünüyor mu

4. **`test_delete_removes_movie`**
   - Film ekle
   - Sil butonuna tıkla
   - Liste boş veya o film yok

### 10.3 — Önemli notlar
- Streamlit re-rendered olduğunda DOM değişir, `page.wait_for_timeout(500)` veya `page.wait_for_selector` kullan
- Her test başında DB'yi temizle (ya backend'e özel `/test/reset` endpoint ekle ki test ortamında çalışsın, ya da test başında tüm film ID'lerini fetch edip sil)
- **Basit çözüm:** Test başında `requests.get(f"{API_URL}/movies")` ile tüm film ID'lerini al, hepsini DELETE et

### 10.4 — Çalıştır
```bash
# Terminal 1
uvicorn src.main:app

# Terminal 2
streamlit run ui/streamlit_app.py

# Terminal 3
pytest tests/e2e/ -v --headed   # tarayıcıyı görmek için
# veya headless:
pytest tests/e2e/ -v
```

## ✅ Kabul Kriteri
- 4 E2E test PASS (headless modda)

### 10.5 — Commit
```bash
git commit -am "test: add e2e tests with playwright for streamlit ui"
```

---

# Faz 11 · GitHub Actions CI/CD (45 dk)

## Hedef
Lint → unit test → integration test → docker build → newman smoke → k8s manifest validate

## Adımlar

### 11.1 — `.github/workflows/ci.yml`

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install ruff
      - run: ruff check src/ tests/ ui/

  test:
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'
      - run: pip install -r requirements-dev.txt
      - run: pytest tests/unit --cov=src --cov-report=xml --cov-fail-under=70
      - name: Upload coverage
        uses: actions/upload-artifact@v4
        with:
          name: coverage-report
          path: coverage.xml

  integration:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'
      - run: pip install -r requirements-dev.txt
      - run: pytest tests/integration -v

  docker-build:
    runs-on: ubuntu-latest
    needs: integration
    steps:
      - uses: actions/checkout@v4
      - name: Build image
        run: docker build -t movie-watchlist:${{ github.sha }} .
      - name: Save image as tar
        run: docker save movie-watchlist:${{ github.sha }} -o image.tar
      - uses: actions/upload-artifact@v4
        with:
          name: docker-image
          path: image.tar

  newman-smoke:
    runs-on: ubuntu-latest
    needs: docker-build
    steps:
      - uses: actions/checkout@v4
      - uses: actions/download-artifact@v4
        with:
          name: docker-image
      - run: docker load -i image.tar
      - name: Start container
        run: |
          docker run -d -p 8000:8000 --name movie-app movie-watchlist:${{ github.sha }}
          # Wait for healthcheck
          for i in {1..30}; do
            if curl -sf http://localhost:8000/health; then
              echo "App is up"; break
            fi
            sleep 2
          done
      - name: Install newman
        run: npm install -g newman
      - name: Run newman
        run: newman run postman/collection.json --env-var "base_url=http://localhost:8000"
      - name: Cleanup
        if: always()
        run: docker rm -f movie-app

  k8s-validate:
    runs-on: ubuntu-latest
    needs: docker-build
    steps:
      - uses: actions/checkout@v4
      - name: Install kubectl
        uses: azure/setup-kubectl@v4
      - name: Validate manifests
        run: |
          for f in k8s/*.yaml; do
            kubectl apply --dry-run=client -f "$f"
          done
```

### 11.2 — Push & gör
```bash
git add .github/
git commit -m "ci: add github actions pipeline"
git push
```

GitHub repo → Actions sekmesinden workflow'u izle.

### 11.3 — Hata aldıysan
- Lint errors → `ruff check --fix` lokal'de çalıştır, commit at
- Test fail → log'lardan oku, fix et
- Newman fail → backend startup süresi uzun olabilir, sleep süresini artır

## ✅ Kabul Kriteri
- GitHub Actions → tüm job'lar yeşil (lint, test, integration, docker-build, newman-smoke, k8s-validate)

### 11.4 — Commit (varsa fixler)
```bash
git commit -am "ci: fix pipeline issues"
git push
```

---

# Faz 12 · Belgeler (60 dk)

## 12.1 — `README.md`

İçerik:
```markdown
# Movie Watchlist

Bulut Mimarilerinde Test Mühendisliği dönem projesi.

## Özellikler
- 8 REST endpoint (FastAPI)
- Streamlit UI
- Multi-stage Docker image
- Kubernetes deployment (Minikube)
- GitHub Actions CI/CD
- Unit + Integration + E2E + Postman testleri

## Kurulum

### Docker Compose ile (önerilen)
\`\`\`bash
docker compose up
\`\`\`
- API: http://localhost:8000/docs
- UI: http://localhost:8501

### Lokal (geliştirme)
\`\`\`bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
uvicorn src.main:app --reload
\`\`\`

### Kubernetes (Minikube)
\`\`\`bash
minikube start
eval $(minikube docker-env)
docker build -t movie-watchlist:latest .
kubectl apply -f k8s/
minikube service movie-watchlist --url
\`\`\`

## Test
\`\`\`bash
pytest                              # tüm testler
pytest --cov=src --cov-report=html  # coverage raporu
newman run postman/collection.json  # API testleri
pytest tests/e2e/                   # E2E (streamlit + uvicorn açık olmalı)
\`\`\`

## Mimari
![Architecture](docs/architecture.png)

## API Örnekleri
... (3-4 curl örneği)

## Demo Video
[YouTube linki](https://...)

## Lisans
MIT
```

## 12.2 — `docs/architecture.png`

🧑 KULLANICI AKSİYONU: Excalidraw veya Draw.io ile çiz. Şu bileşenler olmalı:
- Streamlit UI (sol)
- FastAPI app (orta, 2 replica göster)
- PostgreSQL (sağ)
- Docker katmanı (kutu içinde)
- Kubernetes pod'u (dış kutu)
- GitHub Actions akışı (alt)
- Geliştirici → GitHub → CI → Minikube oku

PNG export et, `docs/architecture.png` olarak kaydet.

## 12.3 — `docs/final-report.pdf`

4-6 sayfa, IEEE benzeri format. Agent şu bölümleri yazsın (Markdown'da, sonra PDF'e dönüştür):

1. **Giriş (½ sf)** — Movie Watchlist seçimi, motivasyon
2. **Mimari (1 sf)** — diyagram + bileşen açıklamaları
3. **Test Stratejisi (1 sf)** — Test piramidi: Unit (en alt, ~20 test), Integration (3), E2E (4), Newman (5). Coverage %.
4. **Pipeline & Deploy (1 sf)** — Actions akışı, K8s manifestleri
5. **Performans & Gözlemlenebilirlik (½ sf)** — *Not: bu projede atlandı, gelecekte Prometheus + Grafana eklenebilir.*
6. **Sonuç & Öğrendiklerim (1 sf)** — sayılar, zorluklar (örn: Minikube image cache, Streamlit selectorları)
7. **(Bireysel olarak yapıyorsan bu bölüm yok)** İş paylaşımı
8. **Kaynaklar** — FastAPI docs, Testcontainers docs, Playwright docs vs.

Markdown'dan PDF için:
```bash
pip install markdown-pdf
markdown-pdf docs/final-report.md -o docs/final-report.pdf
```
Veya kullanıcı manuel Word/Google Docs ile yapabilir.

## 12.4 — `docs/slides.pdf`

🧑 KULLANICI AKSİYONU: 7-8 slayt, Google Slides veya PowerPoint:

1. Kapak — Movie Watchlist + isim + ders
2. Problem & Çözüm
3. Mimari diyagram
4. Test Stratejisi (test piramidi görseli + sayılar)
5. CI/CD Pipeline (GitHub Actions screenshot)
6. Sayılar tablosu (test sayısı, coverage %, build süresi)
7. Demo'dan ekran görüntüleri
8. Öğrendiklerim & Zorluklar

PDF export et → `docs/slides.pdf`

## 12.5 — Demo videosu

🧑 KULLANICI AKSİYONU: 5 dakikalık video, OBS Studio veya Loom ile:
- `docker compose up` → 3 servis ayakta
- Streamlit'te 1 film ekle
- `pytest --cov` çalıştır → coverage göster
- `newman run` göster
- GitHub Actions → son workflow yeşil ekran
- `kubectl get pods` → 2 replica Running

YouTube'a unlisted yükle, linki README'ye koy.

## 12.6 — Son commit
```bash
git add docs/ README.md
git commit -m "docs: add architecture diagram, final report, slides and demo video link"
git push
```

## ✅ Kabul Kriteri
- `docs/` altında: architecture.png, final-report.pdf, slides.pdf var
- README'de tüm bölümler dolu
- Demo video YouTube'a yüklü, link README'de

---

# Faz 13 · Son Kontrol & Teslim (15 dk)

## Checklist (Rubric'e göre)

| Rubric Kalemi | Tamamlandı? |
|---|---|
| Repo + Kod Kalitesi (20p) | ☐ |
| Test Çeşitliliği — unit/integration/e2e (15p) | ☐ |
| CI/CD Pipeline (15p) | ☐ |
| Container & K8s (15p) | ☐ |
| AWS / LocalStack (5p) | ⛔ ATLANDI |
| Monitoring (5p) | ⛔ ATLANDI |
| Performans Raporu (5p) | ⛔ ATLANDI |
| Final Demo + Sunum (15p) | ☐ (sunum gününde) |
| Final Rapor (5p) | ☐ |

**Beklenen puan: 70-85/100**

## Son adımlar

1. Repo'da tüm dosyaların doğru yerde olduğunu kontrol et:
```bash
tree -L 3 -I '.venv|__pycache__|.git|node_modules'
```

2. README'den demo video linki gerçekten çalışıyor mu test et

3. GitHub Actions son commit'te yeşil mi kontrol et

4. `docker compose up` ile tüm sistemin son bir kez ayağa kalktığını doğrula

5. Sunum öncesi:
   - Minikube önceden başlatılmış olsun
   - Docker image'lar build edilmiş olsun
   - Tarayıcıda `/docs` ve Streamlit tab'ları açık olsun
   - Terminal'de komutlar hazır (`pytest`, `newman run`, `kubectl get pods`)

6. Final commit & tag:
```bash
git commit --allow-empty -m "chore: final submission"
git tag v1.0.0
git push origin main --tags
```

---

# Sunum Hazırlığı (Agent yapmaz, kullanıcı için not)

**Q&A için hazırlık** — şartnamenin 8.5 bölümündeki olası sorular:

1. **"Bu kod satırı ne yapıyor?"** — `services/movie_service.py`'deki her fonksiyonu satır satır anlat. Özellikle `update_movie` içindeki `model_dump(exclude_unset=True)` ne işe yarıyor bil.

2. **"Coverage neden buradan düşük?"** — `htmlcov/index.html`'i sunum öncesi aç, eksik satırları gör. Genelde error handler'lar atlanır, normal.

3. **"Dockerfile'da neden multi-stage?"** — Build dependencies (gcc) production image'da olmasın, image küçülsün, attack surface azalsın diye.

4. **"Deploy çökerse rollback nasıl?"** — `kubectl rollout undo deployment/movie-watchlist` veya önceki image tag'ine `kubectl set image` ile dön.

5. **"Neden Streamlit?"** — Hızlı UI prototyping, Python ekosistemi içinde, E2E test için yeterli.

6. **"PostgreSQL yerine neden SQLite kullanmıyorsun production'da?"** — SQLite tek-yazıcı, concurrency yok, K8s'te volume sharing sorunlu.

7. **"Integration test ne için?"** — ORM query'leri PostgreSQL'in gerçek davranışına karşı doğrulamak (SQLite'da olmayan ILIKE, JSON tipi gibi farklar var).

---

**BAŞARILAR! 🎬**
