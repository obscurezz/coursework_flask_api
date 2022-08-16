from project.server import create_app
from project.config import app_config
from set_environment import _set_environ


if __name__ == '__main__':
    _set_environ('DEV')
    app = create_app(app_config)
    app.run()
