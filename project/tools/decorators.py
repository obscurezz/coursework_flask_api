from typing import Callable

import jwt
from flask import request, abort, current_app


def auth_required(func: Callable):
    """
    decorates CBV method with JWT token checking
    :param func: CBV method that we are checking for authorization needed
    """
    def decorator(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)

        auth_data = request.headers['Authorization']
        token = auth_data.split('Bearer ')[-1]

        try:
            current_user = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        except jwt.exceptions.DecodeError as e:
            abort(401)
            return {'Exception': e}

        return func(username=current_user['username'], *args, **kwargs)

    return decorator
