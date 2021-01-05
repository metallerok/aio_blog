import pytest
from pytest_aiohttp import aiohttp_client
from logging import getLogger
import asyncio
from sqlalchemy import create_engine
from models.meta import Base

from main import app_factory
import configparser

config = configparser.ConfigParser()
config_path = "./pytest.ini"
config.read(config_path)

logger = getLogger("aio_blog.tests")
logger.setLevel("INFO")


@pytest.fixture(scope="module")
def event_loop(request):
    loop = asyncio.get_event_loop()

    yield loop

    loop.close()


@pytest.fixture(scope="module")
def create_db():
    logger.info("Creating database")

    db_name = "test_" + config.get("DEFAULT", "db_name")
    db_user = config.get("DEFAULT", "db_user")
    db_password = config.get("DEFAULT", "db_password")
    db_host = config.get("DEFAULT", "db_host")
    db_port = config.get("DEFAULT", "db_port")

    postgres_dsn = f"postgres://{db_user}:{db_password}@{db_host}:{db_port}"

    engine = create_engine(postgres_dsn, isolation_level='AUTOCOMMIT')
    conn = engine.connect()
    conn.execute(f"CREATE DATABASE {db_name}")
    conn.close()

    yield {
        "db_name": db_name,
        "db_user": db_user,
        "db_host": db_host,
        "db_port": db_port,
        "db_password": db_password,
        "db_dsn": postgres_dsn,
        "testing": True,
    }

    logger.info("Destroying database")
    engine = create_engine(postgres_dsn, isolation_level='AUTOCOMMIT')
    conn = engine.connect()
    conn.execute(f"DROP DATABASE {db_name}")
    conn.close()


@pytest.fixture(scope="module")
def create_tables(create_db):
    logger.info("Create tables")
    # engine = create_engine(f"{create_db['db_dsn']}/{create_db['db_name']}")
    # Base.metadata.bind = engine
    # Base.metadata.create_all()


@pytest.fixture(scope="module")
async def create_test_app(create_db):
    app = app_factory(
        global_config=config["DEFAULT"],
        **config['app:main'],
    )

    await app.startup()

    yield app

    await app.shutdown()


@pytest.mark.asyncio
@pytest.fixture
def client(event_loop, create_test_app):
    logger.info("Create test client")
    return event_loop.run_until_complete(aiohttp_client(create_test_app))
