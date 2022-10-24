from project.dao.main_dao import MovieDAO
from project.exceptions import ItemNotFound, BaseServiceError
from project.orm_models import Movie


class MovieService:
    def __init__(self, dao: MovieDAO) -> None:
        self.dao = dao

    def get_movie_by_id(self, pk: int) -> dict:
        if movie := self.dao.select_item_by_pk(pk):
            return movie
        raise ItemNotFound(f'Movie with pk={pk} does not exists.')

    def get_all_movies(self, page: int | None = None, status: str | None = None) -> list[dict]:
        """
        :param page: LIMIT OFFSET parameter
        :param status: if status is NEW we order our statement by 'year' field
        :return: select query with implemented parameters
        """
        if status == 'NEW':
            return self.dao.select_all_items(page=page, order_field='year')
        return self.dao.select_all_items(page=page, order_field=None)

    def get_movie_by_query(self, page: int | None, **kwargs) -> list[dict]:
        if not kwargs:
            return self.get_all_movies(page=page)
        else:
            if movies := self.dao.select_items_by_arguments(**kwargs):
                return movies
            else:
                raise ItemNotFound(f'Movies with such parameters {kwargs.items()} do not exist.')

    def post_movie(self, **kwargs) -> Movie:
        try:
            new_item: Movie = self.dao.insert_item(**kwargs)
            return new_item
        except Exception as e:
            raise BaseServiceError(f'Exception is {e}')

    def put_movie(self, pk: int, **kwargs) -> Movie:
        if update_item := self.dao.update_item_by_pk(pk, **kwargs):
            return update_item
        raise ItemNotFound(f'Movie with pk={pk} does not exists.')

    def delete_movie(self, pk: int) -> Movie:
        if delete_item := self.dao.delete_item_by_pk(pk):
            return delete_item
        raise ItemNotFound(f'Movie with pk={pk} does not exists.')
