# Movie Watchlist

Bulut Mimarilerinde Test Mühendisliği dönem projesi.

## Özellikler

- 8 REST endpoint (FastAPI + SQLAlchemy)
- Streamlit UI (film ekleme, arama, izlendi işaretleme, silme)
- Multi-stage Docker image (~73 MB)
- Kubernetes deployment (Minikube, 2 replica)
- GitHub Actions CI/CD (lint → unit → integration → docker → newman → k8s-validate)
- Unit + Integration + E2E + Postman testleri — coverage **%94**

## Kurulum

### Docker Compose ile (önerilen)

```bash
docker compose up
```

- API: http://localhost:8000/docs
- UI:  http://localhost:8501

### Lokal (geliştirme)

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements-dev.txt
uvicorn src.main:app --reload
# Ayrı terminalde:
streamlit run ui/streamlit_app.py
```

### Kubernetes (Minikube)

```bash
minikube start --driver=docker
eval $(minikube docker-env)   # Windows: minikube docker-env | Invoke-Expression
docker build -t movie-watchlist:latest .
kubectl apply -f k8s/
minikube service movie-watchlist --url
```

## Test

```bash
# Unit testler + coverage
pytest tests/unit --cov=src --cov-report=html

# Integration testler (Docker gerekli)
pytest tests/integration -v

# E2E testler (backend + streamlit açık olmalı)
pytest tests/e2e -v

# Postman / Newman
newman run postman/collection.json
```

## API Örnekleri

```bash
# Sağlık kontrolü
curl http://localhost:8000/health

# Film ekle
curl -X POST http://localhost:8000/movies \
  -H "Content-Type: application/json" \
  -d '{"title":"Inception","director":"Nolan","year":2010,"genre":"Sci-Fi"}'

# Filmleri listele
curl http://localhost:8000/movies

# İzlendi olarak işaretle
curl -X PATCH http://localhost:8000/movies/1 \
  -H "Content-Type: application/json" \
  -d '{"watched":true,"rating":9}'

# İstatistikler
curl http://localhost:8000/stats
```

## Mimari

![Architecture](docs/architecture.png)

## CI/CD Pipeline

```
push → lint (ruff) → unit tests (pytest, %94 cov) → integration (testcontainers)
     → docker build → newman smoke → k8s-validate (kubeconform)
```

## Demo Video

[YouTube linki](https://youtube.com) *(sunum öncesi güncellenecek)*

## Lisans

MIT — [cagdas-karatas](LICENSE)
