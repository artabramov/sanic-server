"""Asyncio session management."""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_scoped_session, async_sessionmaker
from asyncio import current_task


Base = declarative_base()


class SessionCreator:
    """Asyncio scoped session creator."""

    def __init__(self, config):
        """Construct a new SessionCreator class."""
        self.config = config
        self.async_engine = self.create_async_engine()
        self.async_session_factory = self.create_async_session_factory()
        self.async_scoped_session = self.create_async_scoped_session()

    @property
    def connection_string(self):
        """Async connection string for Postgres."""
        return "postgresql+asyncpg://%s:%s@%s:%s/%s" % (
            self.config.POSTGRES_USERNAME, self.config.POSTGRES_PASSWORD, self.config.POSTGRES_HOST,
            self.config.POSTGRES_PORT, self.config.POSTGRES_DATABASE)

    def create_async_engine(self):
        """Create a new async engine instance."""
        return create_async_engine(self.connection_string, echo=True, future=True)

    def create_async_session_factory(self):
        """Create a configurable AsyncSession factory."""
        return async_sessionmaker(self.async_engine, expire_on_commit=False)
    
    def create_async_scoped_session(self):
        """Create a scoped management for AsyncSession objects."""
        return async_scoped_session(self.async_session_factory, scopefunc=current_task)

    def create_session(self):
        """Create AsyncSession object."""
        return self.async_scoped_session()
