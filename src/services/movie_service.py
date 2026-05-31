from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session

from src.models import Movie
from src.schemas import MovieCreate, MovieUpdate


def create_movie(db: Session, movie_data: MovieCreate) -> Movie:
    """Create a new movie and persist it to the database."""
    movie = Movie(**movie_data.model_dump())
    db.add(movie)
    db.commit()
    db.refresh(movie)
    return movie


def get_movies(
    db: Session,
    watched: bool | None = None,
    skip: int = 0,
    limit: int = 100,
) -> list[Movie]:
    """Return a list of movies, optionally filtered by watched status."""
    query = db.query(Movie)
    if watched is not None:
        query = query.filter(Movie.watched == watched)
    return query.offset(skip).limit(limit).all()


def get_movie_by_id(db: Session, movie_id: int) -> Movie | None:
    """Return a single movie by ID, or None if not found."""
    return db.query(Movie).filter(Movie.id == movie_id).first()


def update_movie(
    db: Session,
    movie_id: int,
    update_data: MovieUpdate,
) -> Movie | None:
    """Update a movie's fields. Sets watched_at when watched is set to True."""
    movie = get_movie_by_id(db, movie_id)
    if movie is None:
        return None

    changes = update_data.model_dump(exclude_unset=True)

    if changes.get("watched") is True and not movie.watched:
        changes["watched_at"] = datetime.utcnow()

    for field, value in changes.items():
        setattr(movie, field, value)

    db.commit()
    db.refresh(movie)
    return movie


def delete_movie(db: Session, movie_id: int) -> bool:
    """Delete a movie. Returns True if deleted, False if not found."""
    movie = get_movie_by_id(db, movie_id)
    if movie is None:
        return False
    db.delete(movie)
    db.commit()
    return True


def search_movies(db: Session, query: str) -> list[Movie]:
    """Search movies by title or director (case-insensitive)."""
    pattern = f"%{query.lower()}%"
    return (
        db.query(Movie)
        .filter(
            func.lower(Movie.title).like(pattern)
            | func.lower(Movie.director).like(pattern)
        )
        .all()
    )


def get_stats(db: Session) -> dict:
    """Return aggregate statistics for the movie collection."""
    total = db.query(Movie).count()
    watched_count = db.query(Movie).filter(Movie.watched == True).count()  # noqa: E712
    avg_rating = (
        db.query(func.avg(Movie.rating))
        .filter(Movie.watched == True, Movie.rating.isnot(None))  # noqa: E712
        .scalar()
    )
    return {
        "total": total,
        "watched_count": watched_count,
        "unwatched_count": total - watched_count,
        "avg_rating": float(avg_rating) if avg_rating is not None else None,
    }
