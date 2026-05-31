import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer

from src.database import Base


@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:16") as pg:
        yield pg


@pytest.fixture(scope="session")
def pg_engine(postgres_container):
    engine = create_engine(postgres_container.get_connection_url())
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture(scope="function")
def pg_session(pg_engine):

    Session = sessionmaker(bind=pg_engine)
    session = Session()
    session.execute(text("TRUNCATE TABLE movies RESTART IDENTITY CASCADE"))
    session.commit()
    yield session
    session.close()
