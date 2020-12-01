from sqlalchemy.ext.declarative import declarative_base

from src.lib.sqlalchemy import base_model

Base = declarative_base(cls=base_model())
