import sqlmodel as _sql

from .funcs import db_funcs

import datetime as _date
import typing as _t
import uuid


class PrimaryKey:
    id: uuid.UUID = _sql.Field(
        default_factory=uuid.uuid4, primary_key=True
    )


class CreatedDate:
    created: _date.datetime = _sql.Field(
        default_factory=db_funcs.not_utc_time
    )


class UpdatedDate:
    updated: _t.Optional[_date.datetime] = _sql.Field(
        sa_column_kwargs={"onupdate": db_funcs.not_utc_time}
    )


class Dates(UpdatedDate, CreatedDate):
    pass


class CompleteState:
    complete: bool = _sql.Field(default=False) 
