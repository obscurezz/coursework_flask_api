from project.config import BASE_DIR, DevConfig
from project.server import create_app
from set_environment import _set_environ


class TestConfigs:
    def test_development(self):
        _set_environ('DEV')
        app_config = create_app(DevConfig).config
        assert app_config["TESTING"] is False
        assert app_config["DEBUG"] is True
        assert app_config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///" + BASE_DIR.joinpath('dev_project.db').as_posix()
        assert app_config["SQLALCHEMY_ECHO"] is True
