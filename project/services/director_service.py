from project.dao.base_dao import BaseDAO
from project.exceptions import ItemNotFound
from project.orm_models import Director


class DirectorService:
    def __init__(self, dao: BaseDAO) -> None:
        self.dao = dao

    def get_director_by_id(self, pk: int) -> Director:
        if director := self.dao.select_item_by_pk(pk):
            return director
        raise ItemNotFound(f'Director with pk={pk} not exists.')

    def get_all_directors(self, page: int | None) -> list[Director]:
        return self.dao.select_all_items(page=page, order_field=None)
