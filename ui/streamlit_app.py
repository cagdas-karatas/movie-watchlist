import os

import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://localhost:8000")


def fetch_movies(search: str = "") -> list:
    if search:
        r = requests.get(f"{API_URL}/movies/search", params={"q": search})
    else:
        r = requests.get(f"{API_URL}/movies")
    return r.json() if r.ok else []


def fetch_stats() -> dict:
    r = requests.get(f"{API_URL}/stats")
    return r.json() if r.ok else {"total": 0, "watched_count": 0, "unwatched_count": 0}


def add_movie(title: str, director: str, year: int, genre: str) -> bool:
    r = requests.post(f"{API_URL}/movies", json={
        "title": title, "director": director, "year": year, "genre": genre,
    })
    return r.ok


def mark_watched(movie_id: int) -> bool:
    r = requests.patch(f"{API_URL}/movies/{movie_id}", json={"watched": True})
    return r.ok


def delete_movie(movie_id: int) -> bool:
    r = requests.delete(f"{API_URL}/movies/{movie_id}")
    return r.status_code == 204


st.set_page_config(page_title="Movie Watchlist", page_icon="🎬", layout="wide")
st.title("🎬 Movie Watchlist")

stats = fetch_stats()
col1, col2, col3 = st.columns(3)
col1.metric("Toplam", stats["total"])
col2.metric("İzlenen", stats["watched_count"])
col3.metric("İzlenmemiş", stats["unwatched_count"])

st.markdown('<div id="movie-list"></div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("Yeni Film Ekle")
    with st.form(key="add_movie_form"):
        title = st.text_input("Film Adı", key="input_title")
        director = st.text_input("Yönetmen", key="input_director")
        year = st.number_input("Yıl", min_value=1900, max_value=2030,
                               value=2024, key="input_year")
        genre = st.selectbox("Tür", ["Action", "Drama", "Comedy", "Sci-Fi", "Horror"],
                             key="input_genre")
        submitted = st.form_submit_button("Ekle", use_container_width=True)

    if submitted:
        if not title.strip():
            st.error("Film adı boş olamaz.")
        else:
            if add_movie(title.strip(), director.strip(), int(year), genre):
                st.success(f"'{title}' eklendi!")
                st.rerun()
            else:
                st.error("Film eklenemedi.")

search_query = st.text_input("🔍 Film ara...", key="search_box", placeholder="Başlık veya yönetmen")

movies = fetch_movies(search_query.strip() if search_query else "")

if not movies:
    st.info("Listede film yok." if not search_query else "Arama sonucu bulunamadı.")
else:
    header = st.columns([3, 2, 1, 2, 1, 1, 1])
    for col, label in zip(header, ["Başlık", "Yönetmen", "Yıl", "Tür", "İzlendi", "Puan", ""]):
        col.markdown(f"**{label}**")
    st.divider()

    for movie in movies:
        row = st.columns([3, 2, 1, 2, 1, 1, 1])
        row[0].write(movie["title"])
        row[1].write(movie.get("director") or "-")
        row[2].write(str(movie.get("year") or "-"))
        row[3].write(movie.get("genre") or "-")
        row[4].write("✅" if movie["watched"] else "⬜")
        row[5].write(str(movie.get("rating") or "-"))

        with row[6]:
            if not movie["watched"]:
                if st.button("İzlendi", key=f"watch_{movie['id']}"):
                    mark_watched(movie["id"])
                    st.rerun()
            else:
                if st.button("Sil", key=f"delete_{movie['id']}"):
                    delete_movie(movie["id"])
                    st.rerun()
