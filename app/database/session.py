from app.settings import postgres

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


async_engine = create_async_engine(postgres.async_dsn)
async_session = async_sessionmaker(async_engine, expire_on_commit=False)

sync_engine = create_engine(postgres.dsn)
sync_session = sessionmaker(sync_engine, expire_on_commit=False)
