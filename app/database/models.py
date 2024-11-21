from pydantic import ConfigDict

from .bases import CompleteState
from .enums import Breeds

import sqlmodel as _sql
import uuid


metadata = _sql.SQLModel


config = ConfigDict(use_enum_values=True)


class SpyCatModel(metadata):
    model_config = config

    name: str
    years_experience: int
    breed: Breeds # type: ignore
    salary: int


class TargetModel(metadata):
    name: str
    country: str
    notes: str

    def __hash__(self):
        return hash((self.name, self.country, self.notes))
