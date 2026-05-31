import pytest

from src.schemas import MovieCreate, MovieUpdate
from src.services.movie_service import (
    create_movie,
    delete_movie,
    get_movie_by_id,
    get_movies,
    get_stats,
    search_movies,
    update_movie,
)
from tests.factories import MovieFactory


def test_create_movie_success(db_session):
    data = MovieCreate(title="Inception", director="Nolan", year=2010, genre="Sci-Fi")
    movie = create_movie(db_session, data)
    assert movie.id is not None
    assert movie.title == "Inception"
    assert movie.director == "Nolan"


def test_get_movie_by_id_found(db_session):
    created = MovieFactory(title="The Matrix")
    found = get_movie_by_id(db_session, created.id)
    assert found is not None
    assert found.id == created.id


def test_get_movie_by_id_not_found_returns_none(db_session):
    result = get_movie_by_id(db_session, 9999)
    assert result is None


def test_get_movies_empty_list(db_session):
    result = get_movies(db_session)
    assert result == []


def test_get_movies_filter_by_watched(db_session):
    MovieFactory(watched=True)
    MovieFactory(watched=True)
    MovieFactory(watched=False)

    watched = get_movies(db_session, watched=True)
    assert len(watched) == 2

    unwatched = get_movies(db_session, watched=False)
    assert len(unwatched) == 1


def test_get_movies_pagination(db_session):
    for _ in range(5):
        MovieFactory()

    result = get_movies(db_session, skip=2, limit=2)
    assert len(result) == 2


def test_update_movie_sets_watched_at(db_session):
    movie = MovieFactory(watched=False)
    updated = update_movie(db_session, movie.id, MovieUpdate(watched=True))
    assert updated.watched is True
    assert updated.watched_at is not None


def test_update_movie_partial_only_changes_given_fields(db_session):
    movie = MovieFactory(title="Original Title", rating=None)
    updated = update_movie(db_session, movie.id, MovieUpdate(rating=8))
    assert updated.rating == 8
    assert updated.title == "Original Title"


def test_delete_movie_returns_true_when_exists(db_session):
    movie = MovieFactory()
    result = delete_movie(db_session, movie.id)
    assert result is True
    assert get_movie_by_id(db_session, movie.id) is None


def test_delete_movie_returns_false_when_not_exists(db_session):
    result = delete_movie(db_session, 9999)
    assert result is False


def test_search_movies_by_title(db_session):
    MovieFactory(title="The Dark Knight")
    MovieFactory(title="Interstellar")

    results = search_movies(db_session, "dark knight")
    assert len(results) == 1
    assert results[0].title == "The Dark Knight"


def test_search_movies_by_director(db_session):
    MovieFactory(director="Christopher Nolan", title="Dunkirk")
    MovieFactory(director="Steven Spielberg", title="Jaws")

    results = search_movies(db_session, "nolan")
    assert len(results) == 1
    assert results[0].director == "Christopher Nolan"


def test_get_stats_empty_db(db_session):
    stats = get_stats(db_session)
    assert stats["total"] == 0
    assert stats["watched_count"] == 0
    assert stats["unwatched_count"] == 0
    assert stats["avg_rating"] is None


def test_get_stats_with_movies(db_session):
    MovieFactory(watched=True, rating=8)
    MovieFactory(watched=True, rating=10)
    MovieFactory(watched=False, rating=None)
    MovieFactory(watched=False, rating=None)

    stats = get_stats(db_session)
    assert stats["total"] == 4
    assert stats["watched_count"] == 2
    assert stats["unwatched_count"] == 2
    assert stats["avg_rating"] == pytest.approx(9.0)
