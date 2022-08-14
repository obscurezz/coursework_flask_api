from typing import Type

from flask_sqlalchemy import BaseQuery

from project.dao.base_dao import BaseDAO
from project.orm_models import Movie, Genre, Director, User


class MovieDAO(BaseDAO[Movie]):
    __model__: Type[Movie] = Movie

    def select_items_by_arguments(self, **kwargs) -> list[Movie]:
        stmt: BaseQuery = self._db_session.query(self.__model__).filter_by(**kwargs)
        return stmt


class GenreDAO(BaseDAO[Genre]):
    __model__: Type[Genre] = Genre


class DirectorDAO(BaseDAO[Director]):
    __model__: Type[Director] = Director


class UserDAO(BaseDAO[User]):
    __model__: Type[User] = User
