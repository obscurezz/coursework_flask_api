from typing import Type
from models import BaseModel


class ValidatedModel:
    def __init__(self, cls: Type[BaseModel], model: BaseModel):
        self.cls = cls
        self.model = model

    def _return_validated(self) -> dict:
        return self.cls.from_orm(self.model)
