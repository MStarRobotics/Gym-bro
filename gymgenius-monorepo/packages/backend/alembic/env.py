# flake8: noqa
# pyright: reportMissingImports=false, reportAttributeAccessIssue=false
"""Alembic environment configuration."""
import asyncio
from logging.config import fileConfig

from alembic import context  # type: ignore
from app.config import settings  # type: ignore
from app.db import Base  # type: ignore
from sqlalchemy import pool  # type: ignore
from sqlalchemy.engine import Connection  # type: ignore
from sqlalchemy.ext.asyncio import async_engine_from_config  # type: ignore

# Import models module so Alembic can detect schema changes and register
# SQLAlchemy metadata. We attempt a single import and ignore if models are not
# available yet during project bootstrap.
try:
    import app.models as models  # type: ignore  # noqa: F401
except ImportError:
    pass  # Models may not exist yet during initial setup

# Alembic Config object
config = context.config

# Override sqlalchemy.url from settings
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Add your model's MetaData object here
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """Execute migrations with connection."""
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Run migrations in async mode."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
