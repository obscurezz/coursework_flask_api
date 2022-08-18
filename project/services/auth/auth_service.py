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

    def _generate_tokens(self, email: str, password: str | None, is_refresh: bool = False) -> dict:
        def create_token(timer: str, value: int, data: dict) -> str:
            if timer == 'min':
                time_token = datetime.datetime.utcnow() + datetime.timedelta(minutes=value)
            elif timer == 'days':
                time_token = datetime.datetime.utcnow() + datetime.timedelta(days=value)
            else:
                return 'Wrong time input'

            data['exp'] = calendar.timegm(time_token.timetuple())
            result_token = jwt.encode(data, current_app.config['SECRET_KEY'], algorithm='HS256')
            return result_token

        user = self.user_service.get_user_by_email_and_password(email=email, password=password)
        if not user:
            abort(404)

        if not is_refresh:
            if not compose_passwords(user['password'], password):
                abort(400)

        data = {
            'username': user['email'],
            'password': user['password']
        }

        access_token = create_token('min', 30, data)
        refresh_token = create_token('days', 30, data)

        tokens = TokenModel(access_token=access_token, refresh_token=refresh_token)

        return tokens.dict()

    def _approve_refresh_token(self, refresh_token: str) -> dict:
        data = jwt.decode(refresh_token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        username = data.get('username')

        return self._generate_tokens(username, None, is_refresh=True)
