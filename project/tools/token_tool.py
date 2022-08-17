import calendar
import datetime

import jwt
from flask import current_app


def _generate_tokens(data: dict) -> dict:
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


def check_tokens(tokens: dict) -> bool:
    try:
        jwt.decode(tokens.get('access_token'), current_app.config['SECRET_KEY'], algorithms=['HS256'])
        jwt.decode(tokens.get('refresh_token'), current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return True
    except jwt.exceptions.DecodeError:
        return False
