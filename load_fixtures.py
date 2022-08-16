from contextlib import suppress

from sqlalchemy.exc import IntegrityError

from project.config import app_config
from project.orm_models import Director, Genre, Movie
from project.server import create_app
from project.setup.db import db
from project.utils import read_json_file, load_data


app = create_app(app_config)

if __name__ == '__main__':
    data: dict[str, list[dict]] = read_json_file("fixtures.json")

    with app.app_context():
        load_data(data['directors'], Director)
        load_data(data['genres'], Genre)
        load_data(data['movies'], Movie)
        try:
            db.session.commit()
        except IntegrityError as e:
            print(f'IntegrityError: {e.orig}')
        finally:
            db.session.close()

        with suppress(IntegrityError):
            db.session.commit()
