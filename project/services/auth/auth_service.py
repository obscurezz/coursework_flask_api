import calendar
import datetime

import jwt
from flask import current_app
from flask_restx import abort

from project.models import TokenModel
from project.services.auth import UserService
from project.tools.pass_tool import compose_passwords


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    @staticmethod
    def _create_token(time_delta: datetime.timedelta, data: dict) -> str:
        """
        :param time_delta: delta time from app settings
        :param data: input data with username and password
        :return: access or refresh token
        """
        time_token = datetime.datetime.utcnow() + time_delta
        data['exp'] = calendar.timegm(time_token.timetuple())
        result_token = jwt.encode(data, current_app.config['SECRET_KEY'], algorithm='HS256')
        return result_token

    def _generate_tokens(self, email: str, password: str | None, is_refresh: bool = False) -> TokenModel:
        """
        Generates JWT tokens for user authorization
        :param email: user's email
        :param password: user's password if required for access token
        :param is_refresh: check are we logging in or refreshing user session
        :return: access and refresh tokens pair as validated dictionary
        """
        # getting user and checking if user exists
        user = self.user_service.get_user_by_email_and_password(email=email, password=password)
        if not user:
            abort(404)
        # checking do we need new access token or refresh one
        if not is_refresh:
            if not compose_passwords(user['password'], password):
                abort(400)

        data = {
            'id': user['id'],
            'email': user['email']
        }

        access_token = self._create_token(current_app.config['ACCESS_TOKEN_LIFETIME'], data)
        refresh_token = self._create_token(current_app.config['REFRESH_TOKEN_LIFETIME'], data)
        # validate tokens
        tokens = TokenModel(access_token=access_token, refresh_token=refresh_token)

        return tokens

    def _approve_refresh_token(self, refresh_token: str) -> TokenModel:
        data = jwt.decode(refresh_token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        email = data.get('email')

        return self._generate_tokens(email, None, is_refresh=True)
