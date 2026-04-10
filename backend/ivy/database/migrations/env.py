import sys
import asyncio
from logging.config import fileConfig

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import pool
from alembic import context

# Make your src folder importable
sys.path.append(sys.path[0] + "/ivy")

from models.db_models.base import Base  # your declarative base
from database.db import DATABASE_URL      # optional, if you centralize your DB URL

# Alembic config
config = context.config
fileConfig(config.config_file_name)

target_metadata = Base.metadata  # all your tables

# --- Async migration runner ---
async def run_migrations_online():
    connectable = create_async_engine(DATABASE_URL, poolclass=pool.NullPool)

    async with connectable.connect() as conn:
        async with conn.begin():
            await conn.run_sync(do_run_migrations)

    await connectable.dispose()

def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

if context.is_offline_mode():
    raise RuntimeError("Offline mode not supported for async SQLite")

asyncio.run(run_migrations_online())