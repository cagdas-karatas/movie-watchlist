from sqlalchemy.orm import sessionmaker

from src.schemas import MovieCreate, MovieUpdate
from src.services.movie_service import create_movie, get_movies, update_movie


def test_create_and_retrieve_movie_postgres(pg_session):
    data = MovieCreate(
        title="Blade Runner", director="Scott", year=1982, genre="Sci-Fi"
    )
    movie = create_movie(pg_session, data)

    assert movie.id is not None
    result = pg_session.get(type(movie), movie.id)
    assert result is not None
    assert result.title == "Blade Runner"
    assert result.director == "Scott"


def test_filter_movies_by_watched_postgres(pg_session):
    movies_data = [
        MovieCreate(title=f"Watched {i}", director="Dir", year=2000, genre="Drama")
        for i in range(3)
    ]
    unwatched_data = [
        MovieCreate(title=f"Unwatched {i}", director="Dir", year=2000, genre="Drama")
        for i in range(2)
    ]

    for m in movies_data:
        movie = create_movie(pg_session, m)
        update_movie(pg_session, movie.id, MovieUpdate(watched=True))

    for m in unwatched_data:
        create_movie(pg_session, m)

    watched = get_movies(pg_session, watched=True)
    assert len(watched) == 3

    unwatched = get_movies(pg_session, watched=False)
    assert len(unwatched) == 2


def test_update_persists_to_db_postgres(pg_engine, pg_session):
    data = MovieCreate(
        title="The Godfather", director="Coppola", year=1972, genre="Drama"
    )
    movie = create_movie(pg_session, data)
    movie_id = movie.id

    update_movie(pg_session, movie_id, MovieUpdate(rating=10, watched=True))

    NewSession = sessionmaker(bind=pg_engine)
    new_session = NewSession()
    try:
        refreshed = new_session.get(type(movie), movie_id)
        assert refreshed is not None
        assert refreshed.rating == 10
        assert refreshed.watched is True
        assert refreshed.watched_at is not None
    finally:
        new_session.close()
