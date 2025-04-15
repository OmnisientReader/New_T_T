from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from app.core.config import settings
from app.models.base import Base # Import Base from your models

# Create async engine
async_engine = create_async_engine(
    str(settings.DATABASE_URL),
    echo=True,  # Log SQL queries (optional, good for debugging)
    future=True # Use modern SQLAlchemy 2.0 style
)

# Create async session factory
AsyncSessionFactory = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False, # Keep objects accessible after commit
    autocommit=False,
    autoflush=False,
)

async def init_db():
    """Initialize the database, creating tables if they don't exist."""
    async with async_engine.begin() as conn:
        # In a real-world scenario with Alembic, you might not need this
        # But it's useful for initial setup or testing without migrations
        # await conn.run_sync(Base.metadata.drop_all) # Use with caution!
        await conn.run_sync(Base.metadata.create_all)

# Dependency to get DB session
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency that provides an AsyncSession for each request."""
    async with AsyncSessionFactory() as session:
        try:
            yield session
            # Optional: await session.commit() # Can commit here if preferred
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

# Context manager for standalone scripts or tests
@asynccontextmanager
async def db_session() -> AsyncGenerator[AsyncSession, None]:
     """Provide a transactional scope around a series of operations."""
     async with AsyncSessionFactory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
