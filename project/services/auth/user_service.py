from pydantic import EmailStr, ValidationError

from project.dao.main_dao import UserDAO
from project.exceptions import ItemNotFound, PasswordError
from project.models import UserModel
from project.orm_models import User

from project.tools.pass_tool import generate_password_hash, compose_passwords


class UserService:
    def __init__(self, dao: UserDAO) -> None:
        self.dao = dao

    def get_user_by_id(self, pk: int) -> dict:
        if user := self.dao.select_item_by_pk(pk):
            return user
        raise ItemNotFound(f'User with username with id={pk} not exists.')

    def get_user_by_email_and_password(self, email: str, password: str | None = None) -> dict:
        """
        finds by password only for login event, for refreshing only email needed
        :param email: username
        :param password: password for login or None type
        :return: exact user
        """
        if password:
            hash_password = generate_password_hash(password)
            user = self.dao.select_unique_item_by_arguments(email=email, password=hash_password)
        else:
            user = self.dao.select_unique_item_by_arguments(email=email)
        if user:
            return user
        raise ItemNotFound('No such user in database')

    def patch_user_by_id(self, pk: int, first_name: str, last_name: str, favorite_genre: str | None = None):
        if user := self.dao.update_item_by_pk(pk, first_name=first_name, last_name=last_name,
                                                favorite_genre=favorite_genre):
            return user
        raise ItemNotFound('No such user in database')

    def post_new_user(self, email: EmailStr, password: str, first_name: str, last_name: str):
        """
        :params: all required fields
        :return: new user
        """
        user_model: UserModel = UserModel(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        # hashing user password and changing it in model
        hashpwd = generate_password_hash(user_model.password)
        user_model.password = hashpwd
        try:
            new_user: User = self.dao.insert_item(**user_model.dict())
            return {'operation': 'success', 'id': new_user.id, 'email': new_user.email}
        except ValidationError as ve:
            return {'operation': 'failed', 'text': ve}

    def put_user_new_password(self, pk: int, old_password: str, new_password: str):
        """
        :param pk: users id
        :param old_password: old password
        :param new_password: new password
        :return: user with updated password
        """
        current_user = self.get_user_by_id(pk)
        # check if password is correct
        if compose_passwords(current_user['password'], old_password):
            new_hashpwd = generate_password_hash(new_password)
            # if user password equals to previous one returns fail message
            if current_user['password'] == new_hashpwd:
                raise PasswordError('Password is the same to the previous one')
            self.dao.update_item_password(pk, new_hashpwd)
            return {'operation': 'success', 'id': current_user['id'], 'info': 'password changed'}
        raise PasswordError('Incorrect password')
