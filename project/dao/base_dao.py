from typing import Generic, Optional, TypeVar, Type

from flask import current_app
from flask_sqlalchemy import BaseQuery
from sqlalchemy.orm import scoped_session
from werkzeug.exceptions import NotFound

from project.setup.db.base_model import BaseORM

T = TypeVar('T', bound=BaseORM)


class BaseDAO(Generic[T]):
    __model__: Type[BaseORM] = BaseORM

    def __init__(self, db_session: scoped_session) -> None:
        self._db_session = db_session

    @property
    def _items_per_page(self) -> int:
        return current_app.config['ITEMS_PER_PAGE']

    def select_item_by_pk(self, pk: int) -> Optional[T]:
        return self._db_session.query(self.__model__).get(pk)

    def select_all_items(self, page: Optional[int] = None) -> list[T]:
        stmt: BaseQuery = self._db_session.query(self.__model__)
        if page:
            try:
                return stmt.paginate(page, self._items_per_page).items
            except NotFound:
                return []
        return stmt.all()

    def insert_item(self, **kwargs) -> Optional[T]:
        new_item: Optional[T] = self.__model__(**kwargs)

        with self._db_session.begin():
            self._db_session.add(new_item)
            self._db_session.commit()

        return new_item

    def update_item_by_pk(self, pk: int, **kwargs) -> Optional[T]:
        update_item: Optional[T] = self._db_session.query(self.__model__).get(pk)
        for k, v in kwargs.items():
            setattr(update_item, k, v)

        with self._db_session.begin():
            self._db_session.add(update_item)
            self._db_session.commit()

        return update_item

    def delete_item_by_pk(self, pk: int) -> Optional[T]:
        delete_item: Optional[T] = self._db_session.query(self.__model__).get(pk)

        with self._db_session.begin():
            self._db_session.delete(delete_item)
            self._db_session.commit()

        return delete_item
