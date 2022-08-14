import json
from typing import Type

from project.setup.db.base_model import BaseORM
from project.setup.db import db


def read_json_file(filename: str, encoding: str = 'utf-8') -> list | dict:
    with open(filename, encoding=encoding) as jsonfile:
        return json.load(jsonfile)


def load_data(data: list[dict], model: Type[BaseORM]):
    for item in data:
        item['id'] = item.pop('pk')
        db.session.add(model(**item))
