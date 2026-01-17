from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)
from typing import Annotated


engine: AsyncEngine | None = None

def get_engine():
    global engine
    if engine is None:
        engine = create_async_engine(
            "postgresql+asyncpg://admin:123456@localhost:5432/bs_database",
        )
        return engine
    return engine

async_session_factory = async_sessionmaker(
    get_engine(), autocommit=False, autoflush=False, expire_on_commit=False
)

async def session():
    session = async_session_factory()
    try:
        yield session
    finally:
        await session.close()

Session = Annotated[AsyncSession, Depends(session)]
