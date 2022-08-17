from typing import Callable

import jwt
from flask import request, abort, current_app


def auth_required(func: Callable):
    def decorator(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)

        auth_data = request.headers['Authorization']
        token = auth_data.split('Bearer ')[-1]

        try:
            jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        except jwt.exceptions.DecodeError as e:
            abort(401)
            return {'Exception': e}

        return func(*args, **kwargs)

    return decorator
