from project.dao.base_dao import BaseDAO
from project.exceptions import ItemNotFound


class DirectorService:
    def __init__(self, dao: BaseDAO) -> None:
        self.dao = dao

    def get_director_by_id(self, pk: int) -> dict:
        if director := self.dao.select_item_by_pk(pk):
            return director
        raise ItemNotFound(f'Director with pk={pk} not exists.')

    def get_all_directors(self, page: int | None) -> list[dict]:
        return self.dao.select_all_items(page=page, order_field=None)
