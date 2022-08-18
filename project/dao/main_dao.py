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

    def select_item_by_pk(self, pk: int) -> dict:
        selected_user: User = self._db_session.query(self.__model__).get(pk)
        validated_user: dict = self.__valid__.from_orm(selected_user).dict()

        return validated_user

    def select_unique_item_by_arguments(self, **kwargs) -> dict:
        selected_user: User = self._db_session.query(self.__model__).filter_by(**kwargs).one()
        validated_user: dict = self.__valid__.from_orm(selected_user).dict()
        return validated_user

    def update_item_password(self, pk: int, new_password: str) -> dict:
        current_user: User = self._db_session.query(self.__model__).get(pk)
        current_user.password = new_password
        with self._db_session.begin(subtransactions=True):
            self._db_session.add(current_user)
            self._db_session.commit()

        validated_user: dict = self.__valid__.from_orm(current_user).dict()
        return validated_user
