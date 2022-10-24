import pytest

from project.config import TestConfig
from project.orm_models import Genre, Director, Movie
from project.server import create_app
from project.setup.db import db as database


@pytest.fixture(scope='session')
def app():
    app = create_app(TestConfig)
    with app.app_context():
        yield app


@pytest.fixture
def db(app):
    database.init_app(app)
    database.drop_all()
    database.create_all()
    database.session.commit()

    yield database

    database.session.close()


@pytest.fixture
def client(app, db):
    with app.test_client() as client:
        yield client


@pytest.fixture
def genre(db):
    item = Genre(name="genre")
    db.session.add(item)
    db.session.commit()
    return item


@pytest.fixture
def director(db):
    item = Director(name="director")
    db.session.add(item)
    db.session.commit()
    return item


@pytest.fixture
def movies(db, genre, director):
    movies_list = []
    for i in range(10):
        item = Movie(
            title=f"temp_{i}",
            description=f"description of {i}",
            year=1800+i,
            genre_id=genre.id,
            director_id=director.id
        )
        db.session.add(item)
        movies_list.append(item)
    db.session.commit()
    return movies_list
