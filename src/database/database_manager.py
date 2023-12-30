# db_manager.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.database.models import User, Base

from src.util.context import DATABASE_URL


# Create an Async Engine
engine = create_async_engine(DATABASE_URL, echo=False, pool_size=20)

# Create Async Session
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

# CRUD Operations


async def create_tables():
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_user(user_id: int):
    async with AsyncSessionLocal() as session:
        return await session.get(User, user_id)


async def create_user(user_data: dict):
    async with AsyncSessionLocal() as session:
        new_user = User(**user_data)
        session.add(new_user)
        await session.commit()
        return new_user


async def update_user(user_id: int, user_data: dict):
    async with AsyncSessionLocal() as session:
        user = await session.get(User, user_id)
        if user:
            for key, value in user_data.items():
                setattr(user, key, value)
            await session.commit()
            return user
        return None


async def delete_user(user_id: int):
    async with AsyncSessionLocal() as session:
        user = await session.get(User, user_id)
        if user:
            await session.delete(user)
            await session.commit()
            return user
        return None


async def get_name_score_by_id(user_id: int):
    async with AsyncSessionLocal() as session:
        user = await session.get(User, user_id)
        if user:
            return user.name, user.score
        return None, None


async def create_or_update_user_by_id_name(user_id: int, name: str):
    async with AsyncSessionLocal() as session:
        user = await session.get(User, user_id)
        if not user:
            user = User(id=user_id, name=name)
            session.add(user)
        else:
            user.name = name
        await session.commit()
        return user


async def update_score_by_id(user_id: int, score: int):
    async with AsyncSessionLocal() as session:
        user = await session.get(User, user_id)
        if user:
            user.score = score
            await session.commit()
            return user
        return None


async def get_unlock_id_by_user_id(user_id: int):
    async with AsyncSessionLocal() as session:
        user = await session.get(User, user_id)
        if user:
            return user.unlock_id
        return None


async def update_unlock_id_by_user_id(user_id: int, unlock_id: str):
    async with AsyncSessionLocal() as session:
        user = await session.get(User, user_id)
        if user:
            user.unlock_id = unlock_id
            await session.commit()
            return user
        return None
