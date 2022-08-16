from project.dao.base_dao import BaseDAO
from project.exceptions import ItemNotFound
from project.orm_models import Genre


class GenreService:
    def __init__(self, dao: BaseDAO) -> None:
        self.dao = dao

    def get_genre_by_id(self, pk: int) -> Genre:
        if genre := self.dao.select_item_by_pk(pk):
            return genre
        raise ItemNotFound(f'Genre with pk={pk} not exists.')

    def get_all_genres(self, page: int | None) -> list[Genre]:
        return self.dao.select_all_items(page=page, order_field=None)
