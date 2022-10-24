from sqlalchemy.exc import OperationalError

from project.config import app_config
from project.server import create_app
from project.setup.db import db

if __name__ == '__main__':
    with create_app(app_config).app_context():
        try:
            db.drop_all()
            db.create_all()
        except OperationalError as e:
            print(f'OperationalError: {e.orig}')
