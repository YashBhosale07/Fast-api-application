import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine, pool
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Alembic Config
config = context.config

# Logging setup
if config.config_file_name:
    fileConfig(config.config_file_name)

# Import Base (all your models must be imported somewhere)
from app.main.demo import Base

# Metadata for autogenerate
target_metadata = Base.metadata


def get_sync_database_url():
    """Build SYNC DB URL for Alembic."""
    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")

    return f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


def run_migrations_offline() -> None:
    """Run migrations without DB connection."""
    url = get_sync_database_url()

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations with DB engine."""
    url = get_sync_database_url()

    # Create synchronous engine
    engine = create_engine(url, poolclass=pool.NullPool)

    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,     # Optional: detect column type changes
            compare_server_default=True,  # Optional: detect default changes
        )

        with context.begin_transaction():
            context.run_migrations()


# Run migrations
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
