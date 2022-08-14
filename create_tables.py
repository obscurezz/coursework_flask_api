from sqlalchemy.exc import OperationalError, IntegrityError

from project.config import app_config
from project.orm_models import Director, Genre, Movie
from project.server import create_app
from project.setup.db import db
from project.utils import read_json_file, load_data
from set_environment import _set_environ

if __name__ == '__main__':
    _set_environ("DEV")
    with create_app(app_config).app_context():
        try:
            db.create_all()
        except OperationalError as e:
            print(f'OperationalError: {e.orig}')
        else:
            data: dict[str, list[dict]] = read_json_file("fixtures.json")
            load_data(data['directors'], Director)
            load_data(data['genres'], Genre)
            load_data(data['movies'], Movie)
            try:
                db.session.commit()
            except IntegrityError as e:
                print(f'IntegrityError: {e.orig}')
            finally:
                db.session.close()
