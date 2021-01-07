from app_types.users import UserType
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

from models.meta import metadata
from sqlalchemy import Table, String, Boolean, DateTime, func, Column, Enum as EnumType


user = Table(
    'user', metadata,
    Column('uuid', UUID, nullable=False, primary_key=True, default=lambda _: str(uuid4())),
    Column('login', String, nullable=True, unique=True),
    Column('password', String, nullable=True),
    Column('phone', String, unique=True, nullable=True),
    Column('email', String, nullable=True, unique=True),
    Column('name', String),
    Column('surname', String),
    Column('middle_name', String),
    Column('type', EnumType(UserType), nullable=False),
    Column('active', Boolean, default=True, server_default="True"),
    Column('deleted', Boolean, default=False, server_default="False"),

    # access_level_id = Column(Integer, ForeignKey("access_level.id"))
    # access_level = relation("AccessLevel")
    Column(
        'created',
        DateTime,
        nullable=False,
        default=func.now(),
        server_default=func.now(),
    ),
    Column(
        'updated',
        DateTime,
        nullable=False,
        default=func.now(),
        server_default=func.now(),
        onupdate=func.now(),
    ),
    extend_existing=True,
)
