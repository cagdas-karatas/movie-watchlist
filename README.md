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
```bash
docker compose up
```
- API: http://localhost:8000/docs
- UI: http://localhost:8501

### Lokal (geliştirme)
```bash
python3.11 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
uvicorn src.main:app --reload
```

### Kubernetes (Minikube)
```bash
minikube start
eval $(minikube docker-env)
docker build -t movie-watchlist:latest .
kubectl apply -f k8s/
minikube service movie-watchlist --url
```

## Test
```bash
pytest                              # tüm testler
pytest --cov=src --cov-report=html  # coverage raporu
newman run postman/collection.json  # API testleri
pytest tests/e2e/                   # E2E (streamlit + uvicorn açık olmalı)
```

## Mimari
![Architecture](docs/architecture.png)

## Lisans
MIT
