# database_factory.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


class DatabaseFactory:
    def __init__(self, config):
        self.engine = create_async_engine(config.database_url, echo=False, pool_size=20)
        self.AsyncSessionLocal = sessionmaker(
            bind=self.engine, class_=AsyncSession, expire_on_commit=False
        )

    def get_engine(self):
        return self.engine

    def get_session(self):
        return self.AsyncSessionLocal
