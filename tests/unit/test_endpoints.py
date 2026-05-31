from tests.factories import MovieFactory


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_movie_endpoint_returns_201(client):
    payload = {
        "title": "The Matrix", "director": "Wachowski", "year": 1999, "genre": "Sci-Fi"
    }
    response = client.post("/movies", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "The Matrix"
    assert data["id"] is not None
    assert data["watched"] is False


def test_create_movie_endpoint_invalid_data_returns_422(client):
    response = client.post("/movies", json={})
    assert response.status_code == 422


def test_list_movies_endpoint(client):
    MovieFactory(title="Movie A")
    MovieFactory(title="Movie B")

    response = client.get("/movies")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2


def test_get_movie_not_found_returns_404(client):
    response = client.get("/movies/9999")
    assert response.status_code == 404


def test_patch_movie_endpoint(client):
    movie = MovieFactory(title="Oldboy", watched=False)

    response = client.patch(f"/movies/{movie.id}", json={"watched": True, "rating": 10})
    assert response.status_code == 200
    data = response.json()
    assert data["watched"] is True
    assert data["rating"] == 10
    assert data["watched_at"] is not None


def test_delete_movie_returns_204(client):
    movie = MovieFactory(title="To Delete")

    response = client.delete(f"/movies/{movie.id}")
    assert response.status_code == 204

    response = client.get(f"/movies/{movie.id}")
    assert response.status_code == 404


def test_search_endpoint(client):
    MovieFactory(title="Blade Runner")
    MovieFactory(title="Total Recall")

    response = client.get("/movies/search?q=blade")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Blade Runner"


def test_stats_endpoint(client):
    MovieFactory(watched=True, rating=7)
    MovieFactory(watched=False)

    response = client.get("/stats")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert data["watched_count"] == 1
    assert data["unwatched_count"] == 1
    assert "avg_rating" in data
