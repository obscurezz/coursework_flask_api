from typing import Type

from project.dao.base_dao import BaseDAO
from project.models import MovieModel, GenreModel, DirectorModel, UserModel, BaseModel, UserFavoritesModel
from project.orm_models import Movie, Genre, Director, User, UserFavorites


class MovieDAO(BaseDAO[Movie]):
    __model__: Type[Movie] = Movie
    __valid__: Type[BaseModel] = MovieModel

    def select_items_by_arguments(self, **kwargs) -> list[dict]:
        """
        :param kwargs: rows in movies table with values
        :return: list of validated movies by parameters
        """
        stmt: list[Movie] = self._db_session.query(self.__model__).filter_by(**kwargs).all()
        self._db_session.close()
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
        self._db_session.close()
        validated_user: dict = self.__valid__.from_orm(selected_user).dict()

        return validated_user

    def select_unique_item_by_arguments(self, **kwargs) -> dict:
        """
        Implements method of finding exact user by its email and password in database
        :param kwargs: email, password
        :return: exact user as validated dictionary
        """
        selected_user: User = self._db_session.query(self.__model__).filter_by(**kwargs).one()
        self._db_session.close()
        validated_user: dict = self.__valid__.from_orm(selected_user).dict()
        return validated_user

    def update_item_password(self, pk: int, new_password: str) -> dict:
        """
        :param pk: id of user
        :param new_password: new password
        :return: exact user as validated dictionary with new password
        """
        current_user: User = self._db_session.query(self.__model__).get(pk)
        self._db_session.close()
        current_user.password = new_password
        with self._db_session.begin():
            self._db_session.add(current_user)
            self._db_session.commit()

        validated_user: dict = self.__valid__.from_orm(current_user).dict()
        return validated_user


class FavoriteDAO(BaseDAO[UserFavorites]):
    __model__: Type[UserFavorites] = UserFavorites
    __valid__: Type[UserFavoritesModel] = UserFavoritesModel

    def select_unique_item_id_by_arguments(self, **kwargs) -> int:
        """
        :param kwargs: user_id, movie_id
        :return: id of favorite object in database
        """
        selected_favorite: UserFavorites = self._db_session.query(self.__model__).filter_by(**kwargs).one()
        self._db_session.close()
        validated_favorite: dict = self.__valid__.from_orm(selected_favorite).dict()
        return validated_favorite['id']
