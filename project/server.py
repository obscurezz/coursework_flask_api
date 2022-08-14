from typing import Type

from flask import Flask, jsonify
from flask_cors import CORS

from project.exceptions import BaseServiceError
from project.setup.api import api
from project.setup.db import db

from project.config import BaseConfig


def base_service_error_handler(exception: BaseServiceError):
    return jsonify({'error': str(exception)}), exception.code


def create_app(config_object: Type[BaseConfig]) -> Flask:
    app: Flask = Flask(__name__)
    app.config.from_object(config_object)
    # cors
    CORS(app=app)
    # init app
    db.init_app(app)
    api.init_app(app)

    # error handler
    app.register_error_handler(BaseServiceError, base_service_error_handler)

    return app
