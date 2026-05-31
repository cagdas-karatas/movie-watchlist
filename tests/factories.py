import factory
from factory.alchemy import SQLAlchemyModelFactory

from src.models import Movie


class MovieFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Movie
        sqlalchemy_session_persistence = "commit"

    title = factory.Faker("sentence", nb_words=3)
    director = factory.Faker("name")
    year = factory.Faker("random_int", min=1950, max=2024)
    genre = factory.Faker(
        "random_element",
        elements=["Action", "Drama", "Comedy", "Sci-Fi", "Horror"],
    )
    watched = False
    rating = None
