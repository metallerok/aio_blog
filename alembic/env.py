import venusian
import os

from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool, create_engine

from src import models
from src.models.meta import Base

venusian.Scanner().scan(models)

config = context.config
fileConfig(config.config_file_name)

url = os.environ.get('POSTGRES_DSN') or config.get_main_option("sqlalchemy.url")
engine = create_engine(url)
Base.metadata.bind = engine
target_metadata = Base.metadata


def run_migrations_offline():
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    engine_ = create_engine(
        url,
        poolclass=pool.NullPool
    )

    with engine_.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction() as trans:
            context.execute('SET search_path TO public')
            context.run_migrations()
            trans.commit()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
