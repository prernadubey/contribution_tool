from asyncio import current_task

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base

from components.settings import get_settings

SETTINGS = get_settings()

SQLALCHEMY_DB_URL = "postgresql+asyncpg://{}:{}@{}:{}/{}".format(
    SETTINGS.db_username,
    SETTINGS.db_password,
    SETTINGS.db_host,
    SETTINGS.db_port,
    SETTINGS.db_name,
)

engine = create_async_engine(
    SQLALCHEMY_DB_URL, pool_size=15, max_overflow=-1, pool_recycle=3600, pool_timeout=10
)

async_session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine
)
async_session: async_scoped_session = async_scoped_session(
    session_factory=async_session_factory, scopefunc=current_task
)

SQLAlchemyBase = declarative_base()
