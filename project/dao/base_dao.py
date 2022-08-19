from typing import Generic, Optional, TypeVar, Type

from flask import current_app
from flask_sqlalchemy import BaseQuery
from sqlalchemy.orm import scoped_session
from werkzeug.exceptions import NotFound
from pydantic import ValidationError

from project.setup.db.base_model import BaseORM
from project.models import BaseModel
from project.tools.decorators import dao_exceptions

T = TypeVar('T', bound=BaseORM)


class BaseDAO(Generic[T]):
    """
    *model* is an ORM object
    *valid* is a pydantic validation object
    """
    __model__: Type[BaseORM] = BaseORM
    __valid__: Type[BaseModel] = BaseModel

    def __init__(self, db_session: scoped_session) -> None:
        self._db_session = db_session

    @property
    def _items_per_page(self) -> int:
        return current_app.config['ITEMS_PER_PAGE']

    @dao_exceptions
    def select_item_by_pk(self, pk: int) -> dict | None:
        item: Optional[T] = self._db_session.query(self.__model__).get(pk)
        self._db_session.close()
        validated_item: dict = self.__valid__.from_orm(item).dict()
        return validated_item

    def select_all_items(self, page: int | None, order_field: str | None) -> list[dict]:
        """
        :param page: if page is not None, we create all rows statement, if page exists we return LIMIT "page"
        :param order_field: if order field is not None, we create select query with order by "order_field" desc
        :return: resulted statement with all parameters implemented
        """
        if order_field:
            stmt: BaseQuery = self._db_session.query(self.__model__).order_by(
                getattr(self.__model__, order_field).desc())
        else:
            stmt: BaseQuery = self._db_session.query(self.__model__)

        if page:
            try:
                # list of ORM objects with pagination
                items: list[Optional[T]] = stmt.paginate(page, self._items_per_page).items
                # validate them with pydantic model
                validated_items: list[dict] = [self.__valid__.from_orm(item).dict() for item in items]
                return validated_items
            except NotFound:
                return []
        # list of all ORM objects
        items: list[Optional[T]] = stmt.all()
        self._db_session.close()
        # validate them with pydantic model
        validated_items: list[dict] = [self.__valid__.from_orm(item).dict() for item in items]
        return validated_items

    def insert_item(self, **kwargs) -> Optional[T] | dict:
        """
        :param kwargs: all keywords which have to be implemented to new object
        :return: validated new object
        """
        # validate input rows with pydantic model
        try:
            new_item: BaseModel = self.__valid__(**kwargs)
        except (TypeError, ValidationError) as e:
            return {'Exception': e}

        new_object: Optional[T] = self.__model__(**new_item.dict())

        with self._db_session.begin():
            self._db_session.add(new_object)
            self._db_session.commit()

        return new_object

    @dao_exceptions
    def update_item_by_pk(self, pk: int, **kwargs) -> Optional[T] | dict:
        update_object: Optional[T] = self._db_session.query(self.__model__).get(pk)
        for k, v in kwargs.items():
            setattr(update_object, k, v)

        with self._db_session.begin():
            self._db_session.add(update_object)
            self._db_session.commit()

        return update_object

    @dao_exceptions
    def delete_item_by_pk(self, pk: int) -> Optional[T]:
        delete_item: Optional[T] = self._db_session.query(self.__model__).get(pk)

        with self._db_session.begin():
            self._db_session.delete(delete_item)
            self._db_session.commit()

        return delete_item
