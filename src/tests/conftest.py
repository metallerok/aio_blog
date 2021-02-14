import pytest
import logging
import venusian
from main import app_factory
import configparser
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool

import models
venusian.Scanner().scan(models)


config = configparser.ConfigParser()
config_path = "./pytest.ini"
config.read(config_path)

logger = logging.getLogger("aio_blog.tests")
logger.setLevel("INFO")


def _get_db_dsn_from_config() -> str:
    db_user = config.get("DEFAULT", "db_user")
    db_password = config.get("DEFAULT", "db_password")
    db_host = config.get("DEFAULT", "db_host")
    db_port = config.get("DEFAULT", "db_port")

    postgres_dsn = f"postgres://{db_user}:{db_password}@{db_host}:{db_port}"

    return postgres_dsn


def pytest_configure(config):
    """Flake8 is very verbose by default. Silence it."""
    logging.getLogger("flake8").setLevel(logging.ERROR)


@pytest.fixture(scope="module")
def create_db():
    logger.debug("Creating test database")

    db_name = config.get("DEFAULT", "db_name")
    postgres_dsn = _get_db_dsn_from_config()

    engine = create_engine(
        postgres_dsn,
        isolation_level='AUTOCOMMIT',
    )

    conn = engine.connect()

    try:
        conn.execute(f"CREATE DATABASE {db_name}")
    finally:
        conn.close()

    yield {
        "db_name": db_name,
        "db_dsn": postgres_dsn,
    }

    logger.debug("Destroying test database")

    engine = create_engine(
        postgres_dsn,
        isolation_level='AUTOCOMMIT',
    )

    conn = engine.connect()

    try:
        conn.execute(f"DROP DATABASE {db_name}")
    finally:
        conn.close()


@pytest.fixture(scope="module")
def create_tables(create_db):
    from models.meta import metadata
    logger.debug("Create tables")

    engine = create_engine(
        f"{create_db['db_dsn']}/{create_db['db_name']}",
        poolclass=NullPool,
    )

    metadata.create_all(engine)


@pytest.fixture
def client(loop, aiohttp_client, create_tables):
    logger.debug("Create test client")

    app = app_factory(
        global_config=config["DEFAULT"],
        **config['app:main'],
    )

    return loop.run_until_complete(aiohttp_client(app))
