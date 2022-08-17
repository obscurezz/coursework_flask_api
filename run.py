from project.server import create_app
from project.config import app_config

app = create_app(app_config)

if __name__ == '__main__':
    app.run()
