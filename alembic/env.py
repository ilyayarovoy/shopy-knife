from logging.config import fileConfig
from sqlalchemy import create_engine, pool
from alembic import context
from dotenv import load_dotenv
import os

from backend.database.base import Base
from backend.database import models  # noqa: F401

from pathlib import Path
env_path = Path(__file__).parent.parent / ".env"
print(f"Loading .env from: {env_path}")
print(f"File exists: {env_path.exists()}")
load_dotenv(env_path)

config = context.config

# Берём URL и меняем asyncpg → psycopg2 для синхронного подключения
DATABASE_URL = os.getenv("DATABASE_URL", "")
print(f"DATABASE_URL loaded: {DATABASE_URL}")
DATABASE_URL = DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")
print(f"DATABASE_URL after replace: {DATABASE_URL}")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is empty! Check your .env file")

config.set_main_option("sqlalchemy.url", DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = create_engine(
        DATABASE_URL,
        poolclass=pool.NullPool,
        connect_args={"client_encoding": "utf8"}
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()