from .models import *
from .bases import *

import sqlmodel as _sql
import typing as _t


class SpyCat(SpyCatModel, PrimaryKey, Dates, table=True):
    
    missions: _t.List["Mission"] = _sql.Relationship(
        back_populates="spy_cat",
        sa_relationship_kwargs={
            "lazy": "selectin",
            "primaryjoin": "SpyCat.id==Mission.spy_cat_id",
        },
    )


class Mission(MissionModel, PrimaryKey, Dates, table=True):

    spy_cat: _t.Optional[SpyCat] = _sql.Relationship(
        back_populates="missions",
        sa_relationship_kwargs={
            "lazy": "selectin",
            "primaryjoin": "Mission.spy_cat_id==SpyCat.id",
        },
    )
    targets: _t.List["Target"] = _sql.Relationship(
        back_populates="mission",
        sa_relationship_kwargs={
            "lazy": "selectin",
            "primaryjoin": "Mission.id==Target.mission_id",
        },
    )


class Target(TargetModel, PrimaryKey, Dates, table=True):
    mission: Mission = _sql.Relationship(
        back_populates="targets",
        sa_relationship_kwargs={
            "lazy": "selectin",
            "primaryjoin": "Target.mission_id==Mission.id",
        },
    )
