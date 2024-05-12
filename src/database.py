from typing import Any, Generator, Iterable
from sqlalchemy import Insert, Select, Update, exc
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker

from sqlalchemy.orm import sessionmaker, Session

from src.config import settings

from sqlalchemy.pool import StaticPool

engine = create_async_engine(
    settings.database_url,
    echo=True,
)

async_session = async_sessionmaker(bind=engine, autocommit=False, autoflush=False, expire_on_commit=False)


async def fetch_one(stmt: Select | Insert | Update) -> Iterable[Any] | None:
    async with async_session() as session:
        item = await session.scalars(stmt).first()
    return item


async def fetch_all(stmt: Select | Insert | Update) -> Iterable[Any]:
    async with async_session() as session:
        items = await session.scalars(stmt).all()
    return items


async def upd_one(item: Any) -> Any:
    async with async_session() as session:
        try:
            session.add(item)
            session.commit()
            session.refresh(item)
        except exc.IntegrityError:
            session.rollback()
            raise

    return item