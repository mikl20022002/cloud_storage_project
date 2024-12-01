from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import select
from config import db_settings
from cloud_storage_project.models.models_orm import Base, UserOrm
from cloud_storage_project.models.models_pydantic import CreateUserPyd


async_engine = create_async_engine(db_settings.async_db_url())

async_session_factory = async_sessionmaker(async_engine)

# DEV: func for development/testing only
async def dev_create_tables() -> None:
    async with async_engine.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()

# DEV: func for development/testing only
async def dev_delete_tables() -> None:
    async with async_engine.connect() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.commit()


async def create_user(user: CreateUserPyd) -> None:
    async with async_session_factory() as session:
        user_orm = UserOrm(**user.model_dump())
        session.add(user_orm)
        await session.commit()


async def is_user_exists(username: str) -> bool:
    async with async_session_factory() as session:
        stmt = select(1).where(UserOrm.username == username)
        res = await session.execute(stmt)
        return res.scalar() is not None

async def get_user_data(username: str) -> str | None:
    async with async_session_factory() as session:
        stmt = select(UserOrm).where(UserOrm.username == username)
        res = await session.execute(stmt)
        row = res.fetchone()
        return row[0] if row else None

