"""SQLAlchemy connection pool."""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine
import asyncpg


Base = declarative_base()


class PoolCreator:
    def __init__(self, config):
        self.config = config
    
    def get_connection_string(self, use_asyncpg: bool=False):
        return 'postgresql%s://%s:%s@%s:%s/%s' % (
            "+asyncpg" if use_asyncpg else "", self.config.POSTGRES_USERNAME, self.config.POSTGRES_PASSWORD,
            self.config.POSTGRES_HOST, self.config.POSTGRES_PORT, self.config.POSTGRES_DATABASE)

    async def create_pool(self):
        return await asyncpg.create_pool(self.get_connection_string())
    
    def create_engine(self):
        return create_async_engine(self.get_connection_string(use_asyncpg=True), echo=True, future=True)
