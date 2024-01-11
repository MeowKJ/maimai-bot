# db_manager.py - 数据库管理器。
import asyncio

from sqlalchemy.exc import OperationalError

from src.database.base62_encoder import Base62Encoder
from src.database.database_factory import DatabaseFactory
from src.database.models import User, Base
from src.utils.app_config import config

db_factory = DatabaseFactory(config)
engine = db_factory.get_engine()
AsyncSessionLocal = db_factory.get_session()


def retry_async(retries=3, delay=2, exceptions=(OperationalError,)):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            nonlocal retries, delay
            try_count = 0
            while try_count < retries:
                try:
                    return await func(*args, **kwargs)  # 使用await调用协程函数
                except exceptions as e:
                    try_count += 1
                    if try_count >= retries:
                        raise
                    await asyncio.sleep(delay)  # 等待一段时间后重试

        return wrapper

    return decorator


async def create_tables():
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@retry_async(retries=3, delay=2, exceptions=(OperationalError,))
async def get_name_score_by_id(user_id: str):
    encoded_id = Base62Encoder.encode(user_id)
    async with AsyncSessionLocal() as session:
        user = await session.get(User, encoded_id)
        if user:
            return user.name, user.score
        return None, None


@retry_async(retries=3, delay=2, exceptions=(OperationalError,))
async def create_or_update_user_by_id_name(user_id: str, name: str):
    encoded_id = Base62Encoder.encode(user_id)
    async with AsyncSessionLocal() as session:
        user = await session.get(User, encoded_id)
        if not user:
            user = User(id=encoded_id, name=name)
            session.add(user)
        else:
            user.name = name
        await session.commit()
        return user


@retry_async(retries=3, delay=2, exceptions=(OperationalError,))
async def update_score_by_id(user_id: str, score: int):
    encoded_id = Base62Encoder.encode(user_id)
    async with AsyncSessionLocal() as session:
        user = await session.get(User, encoded_id)
        if user:
            user.score = score
            user.score_update_count += 1  # 增加计数
            await session.commit()
            return user
        return None
