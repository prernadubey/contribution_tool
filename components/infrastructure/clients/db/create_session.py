from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession

from components.infrastructure.clients.db.session import async_session


@asynccontextmanager
async def get_session():
    """
    Get a session object whose lifecycle, commits and flush are managed for you.
    """
    session: AsyncSession = async_session()
    try:
        yield session
        await session.commit()
        await session.flush()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()
