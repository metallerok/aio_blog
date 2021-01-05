from setuptools import setup, find_packages
from src.lib import AppGlobals

requires = [
    'alembic==1.0.0',
    'marshmallow==3.0.0b20',
    'Paste==2.0.3',
    'PasteDeploy==1.5.2',
    'pytest==5.4.0',
    'pytest-flakes==4.0.0',
    'pytest-asyncio==0.14.0',
    'pytest-aiohttp==0.3.0',
    'pytest-pep8==1.0.6',
    'SQLAlchemy==1.3.20',
    'venusian==1.1.0',
    'bcrypt==3.1.7',
    'aioredis',
    'aiohttp==3.7.3',
    'async-timeout==3.0.1',
    'gunicorn==20.0.4',
    'asyncpg',
    'aiopg',
    'asyncpgsa',
]

setup(
    name=AppGlobals.name,
    version=AppGlobals.version,
    packages=find_packages(),
    package_dir={'': 'src'},
    install_requires=requires,
    entry_points={
        'paste.app_factory': [
            'main = main:app_factory',
        ],
    }
)
