from pydantic import EmailStr

from project.dao.base_dao import BaseDAO
from project.exceptions import BaseServiceError, ItemNotFound
from project.models import UserModel
from project.orm_models import User


class UserService:
    def __init__(self, dao: BaseDAO) -> None:
        self.dao = dao

    def get_user_by_id(self, pk: int):
        if user := self.dao.select_item_by_pk(pk):
            return user
        raise ItemNotFound(f'User with pk={pk} not exists.')

    def patch_user_by_id(self, pk: int, first_name: str, last_name: str, favorite_genre: str | None = None):
        user: User = self.dao.update_item_by_pk(pk, first_name=first_name, last_name=last_name,
                                                favorite_genre=favorite_genre)
        return user

    def post_new_user(self, email: EmailStr, password: str, first_name: str, last_name: str):
        user_model: UserModel = UserModel(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        try:
            new_user: User = self.dao.insert_item(**user_model.dict())
            return {'operation': 'success', 'id': new_user.id, 'email': new_user.email}
        except BaseServiceError as e:
            return {'operation': 'failed', 'text': e, 'code': BaseServiceError.code}
