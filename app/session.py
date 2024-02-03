"""Provides Postgres database session object."""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import MetaData


# connection_string = 'postgresql+asyncpg://%s:%s@%s:%s/%s' % (
#     config["POSTGRES_USERNAME"], config["POSTGRES_PASSWORD"], config["POSTGRES_HOST"], config["POSTGRES_PORT"],
#     config["POSTGRES_DATABASE"])

# engine = create_async_engine(
#     connection_string,
#     echo=True,
#     future=True,
# )

# Base = declarative_base()

# def async_session_generator():
#     return sessionmaker(
#         autocommit=config["POSTGRES_AUTOCOMMIT"], autoflush=config["POSTGRES_AUTOFLUSH"],
#         bind=engine, class_=AsyncSession
#     )


# meta = MetaData()
# async def create_tables():
#     a = 1
#     async with engine.begin() as conn:
#         # await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)


# @asynccontextmanager
# async def get_session():
#     try:
#         async_session = async_session_generator()
#         async with async_session() as session:
#             yield session

#     except:
#         await session.rollback()
#         raise

#     finally:
#         await session.close()

Base = declarative_base()


class SessionCreator:
    def __init__(self, config):
        self.config = config
        self.engine = self.create_engine()

    @property
    def connection_string(self):
        return 'postgresql+asyncpg://%s:%s@%s:%s/%s' % (
            self.config.POSTGRES_USERNAME, self.config.POSTGRES_PASSWORD, self.config.POSTGRES_HOST,
            self.config.POSTGRES_PORT, self.config.POSTGRES_DATABASE)

    def async_session_generator(self):
        return sessionmaker(
            autocommit=self.config.POSTGRES_AUTOCOMMIT, autoflush=self.config.POSTGRES_AUTOFLUSH,
            bind=self.engine, class_=AsyncSession
        )

    def create_engine(self):
        return create_async_engine(self.connection_string, echo=True, future=True)

    @asynccontextmanager
    async def get_session(self):
        try:
            async_session = self.async_session_generator()
            async with async_session() as session:
                yield session

        except Exception as e:
            await session.rollback()
            raise

        finally:
            await session.close()
