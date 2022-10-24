from project.dao.base_dao import BaseDAO
from project.exceptions import ItemNotFound


class GenreService:
    def __init__(self, dao: BaseDAO) -> None:
        self.dao = dao

    def get_genre_by_id(self, pk: int) -> dict:
        if genre := self.dao.select_item_by_pk(pk):
            return genre
        raise ItemNotFound(f'Genre with pk={pk} not exists.')

    def get_all_genres(self, page: int | None) -> list[dict]:
        return self.dao.select_all_items(page=page, order_field=None)
