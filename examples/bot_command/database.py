from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

DB_PATH = Path(__file__).with_name("bot.sqlite3")

engine = create_async_engine(f"sqlite+aiosqlite:///{DB_PATH}")
session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
    engine, expire_on_commit=False
)


class Base(DeclarativeBase):
    pass


async def create_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
