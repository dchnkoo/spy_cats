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


class MissionModel(metadata, CompleteState):

    spy_cat_id: uuid.UUID = _sql.Field(
        sa_column=_sql.Column(
            _sql.UUID, _sql.ForeignKey("spycat.id", ondelete="CASCADE")
        )
    )
    

class TargetModel(metadata, CompleteState):
    name: str
    country: str
    notes: str
    mission_id: uuid.UUID = _sql.Field(
        sa_column=_sql.Column(
            _sql.UUID, _sql.ForeignKey("mission.id", ondelete="CASCADE")
        )
    )
