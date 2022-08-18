import calendar
import datetime

import jwt
from flask import abort, current_app

from project.services.auth import UserService
from project.tools.pass_tool import compose_passwords


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def _generate_tokens(self, email: str, password: str | None, is_refresh: bool = False) -> dict:
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

        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data['exp'] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, current_app.config['SECRET_KEY'], algorithm='HS256')

        days30 = datetime.datetime.utcnow() + datetime.timedelta(days=30)
        data['exp'] = calendar.timegm(days30.timetuple())
        refresh_token = jwt.encode(data, current_app.config['SECRET_KEY'], algorithm='HS256')

        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }

    def _approve_refresh_token(self, refresh_token: str) -> dict:
        data = jwt.decode(refresh_token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        username = data.get('username')

        return self._generate_tokens(username, None, is_refresh=True)
