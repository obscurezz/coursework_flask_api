import os
from pathlib import Path
from typing import Type
from project.utils import read_json_file
from datetime import timedelta


BASE_DIR: Path = Path(__file__).resolve().parent.parent
SECURITY_SETTINGS: dict = read_json_file(BASE_DIR.joinpath('security.json').as_posix())


class BaseConfig(object):
    # security
    PWD_SALT: bytes = SECURITY_SETTINGS['PWD_SALT'].encode('utf-8')
    PWD_HASH_NAME: str = SECURITY_SETTINGS['PWD_HASH_NAME']
    PWD_HASH_ITERATIONS: int = SECURITY_SETTINGS['PWD_HASH_ITERATIONS']

    # pagination
    ITEMS_PER_PAGE = 12

    # os
    SECRET_KEY = b'm=+Y(L1!idBB'

    # json
    RESTX_JSON = {'ensure_ascii': False}
    JSON_SORT_KEYS = False
    JSON_AS_ASCII = False

    # SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # token lifetime
    ACCESS_TOKEN_LIFETIME = timedelta(minutes=30)
    REFRESH_TOKEN_LIFETIME = timedelta(days=30)


class TestConfig(BaseConfig):
    # Test
    TESTING = True

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class DevConfig(BaseConfig):
    # Dev
    DEBUG = True
    ENV = 'development'
    PORT = 5000

    # SQLAlchemy
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + BASE_DIR.joinpath('dev_project.db').as_posix()


class ProdConfig(BaseConfig):
    # Prod
    DEBUG = False
    ENV = 'production'
    PORT = 80

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = "postgresql://$DB_USER:$DB_PASSWORD@$DB_SERVER:5432/$DB_NAME"


class ConfigFactory:
    flask_env = os.getenv('FLASK_ENV')

    @classmethod
    def get_config(cls) -> Type[BaseConfig]:
        match cls.flask_env:
            case 'development':
                return DevConfig
            case 'production':
                return ProdConfig
            case 'testing':
                return TestConfig
            case _:
                raise NotImplementedError


app_config = ConfigFactory.get_config()
