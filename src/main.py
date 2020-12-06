from aiohttp import web
from aiopg.sa import create_engine
import os
import venusian
from paste.deploy import appconfig
from resources.api.v1 import routes
from resources import api
from middleware.logging import logging


CONFIG_FILE_ERROR = 'Ошибка чтения конфигурационного файла!'


def get_config(path: str) -> dict:
    try:
        config = appconfig('config:%s' % path, relative_to=os.getcwd())
    except Exception:
        raise Exception(CONFIG_FILE_ERROR)

    return config


def init_app(config):
    app = web.Application(
        middlewares=[
            logging
        ]
    )
    app['config'] = config
    return app


async def init_db(app):
    postgres_dsn = os.environ.get('POSTGRES_DSN') or app["config"].get('postgres_sqlalchemy_dsn')
    engine = await create_engine(postgres_dsn)
    app['db'] = engine


async def close_db(app):
    app['db'].close()
    await app['db'].wait_closed()


def app_factory(global_config, **config):
    app = init_app(config)
    app.on_startup.append(init_db)
    app.on_cleanup.append(close_db)
    venusian.Scanner().scan(api)
    app.add_routes(routes)
    return app
