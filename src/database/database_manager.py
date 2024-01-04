# db_manager.py - 数据库管理器。

from src.database.base62_encoder import Base62Encoder
from src.database.database_factory import DatabaseFactory
from src.database.models import User, Base
from src.utils.app_config import config

db_factory = DatabaseFactory(config)
engine = db_factory.get_engine()
AsyncSessionLocal = db_factory.get_session()


async def create_tables():
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_name_score_by_id(user_id: str):
    encoded_id = Base62Encoder.encode(user_id)
    async with AsyncSessionLocal() as session:
        user = await session.get(User, encoded_id)
        if user:
            return user.name, user.score
        return None, None


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


# async def get_unlock_id_by_user_id(user_id: str):
#     encoded_id = Base62Encoder.encode(user_id)
#     async with AsyncSessionLocal() as session:
#         user = await session.get(User, encoded_id)
#         if user:
#             return user.unlock_id
#         return None
#
#
# async def update_unlock_id_by_user_id(user_id: str, unlock_id: str):
#     encoded_id = Base62Encoder.encode(user_id)
#     async with AsyncSessionLocal() as session:
#         user = await session.get(User, encoded_id)
#         if user:
#             user.unlock_id = unlock_id
#             await session.commit()
#             return user
#         return None
