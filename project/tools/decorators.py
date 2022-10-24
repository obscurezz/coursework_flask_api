from functools import wraps
from typing import Callable

import jwt
from flask import request, abort, current_app
from pydantic import ValidationError
from sqlalchemy.exc import NoResultFound


def auth_required(func: Callable):
    """
    decorates CBV method with JWT token checking
    :param func: CBV method that we are checking for authorization needed
    """
    @wraps(func)
    def decorator(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)

        auth_data = request.headers['Authorization']
        token = auth_data.split('Bearer ')[-1]

        try:
            current_user = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            return func(email=current_user['email'], *args, **kwargs)
        except jwt.exceptions.DecodeError:
            abort(401)

    return decorator


def dao_exceptions(func: Callable):
    """
    decorates all sql statements that could return No data found or Validation Error
    :param func: SQL select/update/delete method
    """
    @wraps(func)
    def decorator(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (NoResultFound, ValidationError):
            return None

    return decorator
