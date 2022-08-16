import pytest

from project.dao.main_dao import GenreDAO
from project.orm_models import Genre


class TestGenresDAO:

    @pytest.fixture
    def genres_dao(self, db):
        return GenreDAO(db.session)

    @pytest.fixture
    def genre_1(self, db):
        g = Genre(name="Боевик")
        db.session.add(g)
        db.session.commit()
        return g

    @pytest.fixture
    def genre_2(self, db):
        g = Genre(name="Комедия")
        db.session.add(g)
        db.session.commit()
        return g

    def test_get_genre_by_id(self, genre_1, genres_dao):
        assert genres_dao.select_item_by_pk(genre_1.id) == genre_1

    def test_get_genre_by_id_not_found(self, genres_dao):
        assert not genres_dao.select_item_by_pk(1)

    def test_get_all_genres(self, genres_dao, genre_1, genre_2):
        assert genres_dao.select_all_items(page=None, order_field=None) == [genre_1, genre_2]

    def test_get_genres_by_page(self, app, genres_dao, genre_1, genre_2):
        app.config['ITEMS_PER_PAGE'] = 1
        assert genres_dao.select_all_items(page=1, order_field=None) == [genre_1]
        assert genres_dao.select_all_items(page=2, order_field=None) == [genre_2]
        assert genres_dao.select_all_items(page=3, order_field=None) == []
