import pytest

from project.dao.main_dao import DirectorDAO
from project.orm_models import Director


class TestGenresDAO:

    @pytest.fixture
    def directors_dao(self, db):
        return DirectorDAO(db.session)

    @pytest.fixture
    def director_1(self, db):
        d = Director(name="Стэнли Кубрик")
        db.session.add(d)
        db.session.commit()
        return d

    @pytest.fixture
    def director_2(self, db):
        d = Director(name="Кемп Пауэрс")
        db.session.add(d)
        db.session.commit()
        return d

    def test_get_director_by_id(self, director_1, directors_dao):
        assert directors_dao.select_item_by_pk(director_1.id) == director_1

    def test_get_director_by_id_not_found(self, directors_dao):
        assert not directors_dao.select_item_by_pk(1)

    def test_get_all_directors(self, directors_dao, director_1, director_2):
        assert directors_dao.select_all_items(page=None, order_field=None) == [director_1, director_2]

    def test_get_directors_by_page(self, app, directors_dao, director_1, director_2):
        app.config['ITEMS_PER_PAGE'] = 1
        assert directors_dao.select_all_items(page=1, order_field=None) == [director_1]
        assert directors_dao.select_all_items(page=2, order_field=None) == [director_2]
        assert directors_dao.select_all_items(page=3, order_field=None) == []

