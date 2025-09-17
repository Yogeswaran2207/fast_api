import asyncio
from logging.config import fileConfig
import sys
import os

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from alembic import context
from sqlmodel import SQLModel

# Add src folder to PYTHONPATH to resolve imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Import your models so Alembic can see them
from src.fast_api.db.user_model import User
from src.fast_api.db.book_model import Book
from src.fast_api.config import config as app_config  # your config file with DATABASE_URL

# Alembic Config object
alembic_config = context.config

# Interpret the config file for Python logging.
if alembic_config.config_file_name is not None:
    fileConfig(alembic_config.config_file_name)

# Set target_metadata for 'autogenerate'
target_metadata = SQLModel.metadata

# Get your async database URL from your app config
DATABASE_URL = app_config.database_url  # e.g. postgresql+asyncpg://user:pass@localhost:5432/dbname


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    """Run migrations with a connection."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Run migrations in 'online' mode with AsyncEngine."""
    connectable: AsyncEngine = create_async_engine(
        DATABASE_URL,
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
