"""Provides Postgres database session object."""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine
from asyncpg import create_pool


class Pool:
    def __init__(self, config):
        self.config = config
        self.base = declarative_base()

    async def create_pool(self):
        return create_pool(self.connection_string)

    @property
    def connection_string(self):
        return 'postgresql+asyncpg://%s:%s@%s:%s/%s' % (
            self.config.POSTGRES_USERNAME, self.config.POSTGRES_PASSWORD, self.config.POSTGRES_HOST,
            self.config.POSTGRES_PORT, self.config.POSTGRES_DATABASE)

    @property
    def engine(self):
        return create_async_engine(self.connection_string, echo=True, future=True)

