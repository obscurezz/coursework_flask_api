from typing import Type

from project.dao.base_dao import BaseDAO
from project.models import MovieModel, GenreModel, DirectorModel, UserModel, BaseModel
from project.orm_models import Movie, Genre, Director, User


class MovieDAO(BaseDAO[Movie]):
    __model__: Type[Movie] = Movie
    __valid__: Type[BaseModel] = MovieModel

    def select_items_by_arguments(self, **kwargs) -> list[dict]:
        stmt: list[Movie] = self._db_session.query(self.__model__).filter_by(**kwargs).all()
        validated_items: list = [self.__valid__.from_orm(item) for item in stmt]
        return validated_items


class GenreDAO(BaseDAO[Genre]):
    __model__: Type[Genre] = Genre
    __valid__: Type[BaseModel] = GenreModel


class DirectorDAO(BaseDAO[Director]):
    __model__: Type[Director] = Director
    __valid__: Type[BaseModel] = DirectorModel


class UserDAO(BaseDAO[User]):
    __model__: Type[User] = User
    __valid__: Type[BaseModel] = UserModel
