from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from src.lib.sqlalchemy import CustomQuery, base_model

Base = declarative_base(cls=base_model())
