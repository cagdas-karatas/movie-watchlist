import os

import requests

API_URL = os.getenv("API_URL", "http://localhost:8000")
STREAMLIT_URL = os.getenv("STREAMLIT_URL", "http://localhost:8501")
TIMEOUT = 12000


def cleanup_db():
    movies = requests.get(f"{API_URL}/movies").json()
    for m in movies:
        requests.delete(f"{API_URL}/movies/{m['id']}")


def wait_for_app(page):
    page.wait_for_load_state("networkidle")
    page.wait_for_selector("[data-testid='stApp']", timeout=TIMEOUT)
    page.wait_for_timeout(1500)


def add_movie_via_ui(page, title: str, director: str = "Test Dir", year: int = 2023):
    page.get_by_label("Film Adı").fill(title)
    page.get_by_label("Yönetmen").fill(director)
    page.get_by_role("spinbutton").fill(str(year))
    page.get_by_role("button", name="Ekle").click()
    page.wait_for_timeout(2500)


def test_add_movie_appears_in_list(page):
    """Streamlit formu üzerinden eklenen film listede görünmeli."""
    cleanup_db()
    page.goto(STREAMLIT_URL)
    wait_for_app(page)

    add_movie_via_ui(page, "Test Movie E2E")

    page.wait_for_selector("text=Test Movie E2E", timeout=TIMEOUT)
    assert page.locator("text=Test Movie E2E").is_visible()


def test_mark_movie_as_watched_updates_stats(page):
    """API üzerinden izlendi işaretlenen film UI'da ✅ olarak görünmeli."""
    cleanup_db()
    r = requests.post(f"{API_URL}/movies", json={
        "title": "Watch Me Film", "director": "Dir", "year": 2020, "genre": "Drama"
    })
    movie_id = r.json()["id"]
    requests.patch(f"{API_URL}/movies/{movie_id}", json={"watched": True, "rating": 8})

    page.goto(STREAMLIT_URL)
    wait_for_app(page)

    page.wait_for_selector("text=Watch Me Film", timeout=TIMEOUT)
    assert page.locator("text=Watch Me Film").is_visible()
    assert page.locator("text=✅").is_visible()

    stats = requests.get(f"{API_URL}/stats").json()
    assert stats["watched_count"] == 1


def test_search_filters_movies(page):
    """Arama kutusu yalnızca eşleşen filmleri göstermeli."""
    cleanup_db()
    page.goto(STREAMLIT_URL)
    wait_for_app(page)

    add_movie_via_ui(page, "Unique Alpha Film")
    add_movie_via_ui(page, "Completely Different Beta")

    page.wait_for_selector("text=Unique Alpha Film", timeout=TIMEOUT)
    page.wait_for_selector("text=Completely Different Beta", timeout=TIMEOUT)

    search_box = page.get_by_placeholder("Başlık veya yönetmen")
    search_box.click(click_count=3)
    search_box.type("Unique Alpha", delay=100)
    search_box.press("Enter")
    page.wait_for_timeout(4000)

    # Arama API doğrulaması
    search_result = requests.get(
        f"{API_URL}/movies/search", params={"q": "Unique Alpha"}
    ).json()
    assert len(search_result) == 1
    assert search_result[0]["title"] == "Unique Alpha Film"

    assert page.locator("text=Unique Alpha Film").is_visible()
    assert not page.locator("text=Completely Different Beta").is_visible()


def test_delete_removes_movie(page):
    """API üzerinden silinen film UI'da görünmemeli."""
    cleanup_db()
    r = requests.post(f"{API_URL}/movies", json={
        "title": "Delete Me Film", "director": "Dir", "year": 2021, "genre": "Action"
    })
    movie_id = r.json()["id"]

    page.goto(STREAMLIT_URL)
    wait_for_app(page)

    page.wait_for_selector("text=Delete Me Film", timeout=TIMEOUT)
    assert page.locator("text=Delete Me Film").is_visible()

    requests.delete(f"{API_URL}/movies/{movie_id}")

    page.reload()
    wait_for_app(page)

    assert not page.locator("text=Delete Me Film").is_visible()
