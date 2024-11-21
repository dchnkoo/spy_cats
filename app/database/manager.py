from .session import async_session
from pydantic import BaseModel

from sqlalchemy import exc
import sqlmodel as _sql

import typing as _t
import uuid


_T = _t.TypeVar("_T", bound=BaseModel)


class TableManager(_t.Generic[_T]):

    if _t.TYPE_CHECKING:
        id: uuid.UUID

    @classmethod
    async def create_table(cls, data: _T | dict):
        async with async_session() as session:
            try:
                instance = cls(**(data.model_dump() if not isinstance(data, dict) else data))
                session.add(instance)
                await session.commit()
                return instance
            except exc.IntegrityError:
                await session.rollback()
    
    @classmethod
    async def load_instance(cls, id: uuid.UUID):
        async with async_session() as session:
            instance = await session.get(cls, id)
            assert instance is not None, f"404: {cls.__name__} not found."
            return instance

    async def remove(self) -> bool:
        async with async_session() as session:
            try:
                query = _sql.delete(self.__class__).where(self.__class__.id == self.id)
                await session.execute(query)
                await session.commit()
                return True
            except exc.IntegrityError:
                await session.rollback()
                return False
    
    @classmethod
    async def remove_by_id(cls, id: uuid.UUID) -> bool:
        instance = await cls.load_instance(id)
        return await instance.remove()

    @classmethod
    async def get_all(cls):
        async with async_session() as session:
            query = _sql.select(cls)
            results = await session.execute(query)
            return results.scalars().all()
        
    async def update_field(self, field: str, value: _t.Any) -> bool:
        async with async_session() as session:
            try:
                query = _sql.update(self.__class__)\
                    .values({field: value})\
                    .where(self.__class__.id == self.id)
                await session.execute(query)
                await session.commit()
                return True
            except exc.IntegrityError:
                await session.rollback()
                return False
