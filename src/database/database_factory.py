from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

class DatabaseFactory:
    def __init__(self, config):
        # Update to use SQLite for a local database
        self.engine = create_async_engine(
            "sqlite+aiosqlite:///local_db.sqlite",  # Path to your local SQLite file
            echo=False,
            # Removed pool_size and max_overflow, as they're not valid for aiosqlite
        )

        self.AsyncSessionLocal = sessionmaker(
            bind=self.engine, class_=AsyncSession, expire_on_commit=False
        )

    def get_engine(self):
        return self.engine

    def get_session(self):
        return self.AsyncSessionLocal
