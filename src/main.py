from aiohttp import web
from aiopg.sa import create_engine
import os
from paste.deploy import appconfig
from src.resources.api.v1 import api_info
from src.resources.api.v1 import users


CONFIG_FILE_ERROR = 'Ошибка чтения конфигурационного файла!'


def get_config(path: str) -> dict:
    try:
        config = appconfig('config:%s' % path, relative_to=os.getcwd())
    except Exception:
        raise Exception(CONFIG_FILE_ERROR)

    return config


def init_app(config):
    app = web.Application()
    app['config'] = config
    return app


async def init_db(app):
    postgres_dsn = os.environ.get('POSTGRES_DSN') or app["config"].get('postgres_sqlalchemy_dsn')
    engine = await create_engine(postgres_dsn)
    app['db'] = engine


async def close_db(app):
    app['db'].close()
    await app['db'].wait_closed()


def main(config_path: str):
    config = get_config(config_path)
    app = init_app(config)
    app.on_startup.append(init_db)
    app.on_cleanup.append(close_db)
    app.router.add_route('*', '/api_info', api_info.ApiInfoController, name='api_info')
    app.router.add_route('*', '/api/v1/users', users.UsersCollectionController, name='users')
    web.run_app(app)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="Provide path to config file")
    args = parser.parse_args()

    if args.config:
        main(args.config)
    else:
        parser.print_help()
