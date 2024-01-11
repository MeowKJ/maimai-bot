# database_factory.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool


class DatabaseFactory:
    def __init__(self, config):
        self.engine = create_async_engine(
            config.database_url,
            echo=False,
            pool_size=20,  # 根据需要调整
            max_overflow=10,  # 新增参数
            poolclass=QueuePool,  # 显式指定连接池类型
        )

        self.AsyncSessionLocal = sessionmaker(
            bind=self.engine, class_=AsyncSession, expire_on_commit=False
        )

    def get_engine(self):
        return self.engine

    def get_session(self):
        return self.AsyncSessionLocal
