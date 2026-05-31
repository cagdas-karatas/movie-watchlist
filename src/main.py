from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from src.database import get_db, init_db
from src.schemas import MovieCreate, MovieResponse, MovieUpdate, StatsResponse
from src.services.movie_service import (
    create_movie,
    delete_movie,
    get_movie_by_id,
    get_movies,
    get_stats,
    search_movies,
    update_movie,
)

app = FastAPI(title="Movie Watchlist API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/movies", response_model=MovieResponse, status_code=201)
def create_movie_endpoint(movie: MovieCreate, db: Session = Depends(get_db)):
    return create_movie(db, movie)


@app.get("/movies", response_model=list[MovieResponse])
def list_movies_endpoint(
    watched: bool | None = Query(default=None),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return get_movies(db, watched=watched, skip=skip, limit=limit)


@app.get("/movies/search", response_model=list[MovieResponse])
def search_movies_endpoint(
    q: str = Query(min_length=1),
    db: Session = Depends(get_db),
):
    return search_movies(db, q)


@app.get("/movies/{movie_id}", response_model=MovieResponse)
def get_movie_endpoint(movie_id: int, db: Session = Depends(get_db)):
    movie = get_movie_by_id(db, movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie


@app.patch("/movies/{movie_id}", response_model=MovieResponse)
def update_movie_endpoint(
    movie_id: int,
    update_data: MovieUpdate,
    db: Session = Depends(get_db),
):
    movie = update_movie(db, movie_id, update_data)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie


@app.delete("/movies/{movie_id}", status_code=204)
def delete_movie_endpoint(movie_id: int, db: Session = Depends(get_db)):
    if not delete_movie(db, movie_id):
        raise HTTPException(status_code=404, detail="Movie not found")


@app.get("/stats", response_model=StatsResponse)
def stats_endpoint(db: Session = Depends(get_db)):
    return get_stats(db)
