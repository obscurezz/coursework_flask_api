import os
from pathlib import Path
from typing import Type


BASE_DIR: Path = Path(__file__).resolve().parent.parent


class BaseConfig(object):
    # pagination
    ITEMS_PER_PAGE = 10

    # os
    SECRET_KEY = os.urandom(12)

    # json
    RESTX_JSON = {'ensure_ascii': False}
    JSON_SORT_KEYS = False
    JSON_AS_ASCII = False

    # SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False


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
    PORT = 8080

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + BASE_DIR.joinpath('prod_project.db').as_posix()


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
