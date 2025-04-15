import os
import sys
from logging.config import fileConfig
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import pool

from alembic import context
from dotenv import load_dotenv




dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

config = context.config


if config.config_file_name is not None:
    fileConfig(config.config_file_name)


sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))


from app.models.base import Base

from app.models import table, reservation


target_metadata = Base.metadata


db_url = os.getenv("DATABASE_URL")
if db_url is None:

    raise ValueError(
        "Environment variable DATABASE_URL is not set. "
        "Please ensure it is defined in your .env file and loaded correctly."
    )


async def run_migrations_online() -> None:

    connectable = create_async_engine(
        db_url,
        poolclass=pool.NullPool,
        future=True,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

def do_run_migrations(connection):
     context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
    )

     with context.begin_transaction():
         context.run_migrations()


if context.is_offline_mode():

    raise NotImplementedError("Offline mode not configured for async")
else:
    import asyncio
    asyncio.run(run_migrations_online())
