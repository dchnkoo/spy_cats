from .manager import TableManager, async_session
from .models import *
from .bases import *

import sqlmodel as _sql
import typing as _t


class SpyCat(SpyCatModel, PrimaryKey, Dates, TableManager[SpyCatModel], table=True):

    missions: _t.List["Mission"] = _sql.Relationship(
        back_populates="spy_cat",
        sa_relationship_kwargs={
            "lazy": "selectin",
            "primaryjoin": "SpyCat.id==Mission.spy_cat_id",
        },
    )


class Mission(metadata, PrimaryKey, CompleteState, Dates, TableManager["Mission"], table=True):

    async def tasks(self):
        async with async_session() as session:
            query = _sql.select(Target).where(Target.mission_id == self.id)
            res = await session.execute(query)
            return res.scalars().all()
    
    async def all_tasks_complete(self):
        targets = await self.tasks()
        for target in targets:
            if not target.complete:
                break
        else:
            await self.update_field("complete", True)
            return True
        return False

    spy_cat_id: _t.Optional[uuid.UUID] = _sql.Field(
        sa_column=_sql.Column(
            _sql.UUID, _sql.ForeignKey("spycat.id", ondelete="CASCADE")
        )
    )
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


class Target(TargetModel, PrimaryKey, CompleteState, Dates, TableManager[TargetModel], table=True):
    mission_id: uuid.UUID = _sql.Field(
        sa_column=_sql.Column(
            _sql.UUID, _sql.ForeignKey("mission.id", ondelete="CASCADE")
        )
    )
    mission: Mission = _sql.Relationship(
        back_populates="targets",
        sa_relationship_kwargs={
            "lazy": "selectin",
            "primaryjoin": "Target.mission_id==Mission.id",
        },
    )
