import bcrypt
from src.models.meta import Base
from enum import Enum
from sqlalchemy import Column, func
from sqlalchemy.sql.sqltypes import (
    String,
    Enum as EnumType,
    Boolean,
    DateTime
)
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4


class UserType(Enum):
    ADMIN = 1
    USER = 2
    EXTERNAL_SYSTEM = 3

    @classmethod
    def list(cls):
        return list(map(lambda c: c.name, cls))


class User(Base):
    __tablename__ = "user"

    uuid = Column(UUID, nullable=False, primary_key=True, default=lambda _: str(uuid4()))

    login = Column(String, nullable=True, unique=True)
    password = Column(String, nullable=True)

    phone = Column(String, unique=True, nullable=True)
    email = Column(String, nullable=True, unique=True)

    name = Column(String)
    surname = Column(String)
    middle_name = Column(String)

    type = Column(EnumType(UserType), nullable=False)

    active = Column(Boolean, default=True, server_default="True")
    deleted = Column(Boolean, default=False, server_default="False")

    # access_level_id = Column(Integer, ForeignKey("access_level.id"))
    # access_level = relation("AccessLevel")

    created = Column(
        DateTime,
        nullable=False,
        default=func.now(),
        server_default=func.now(),
    )

    updated = Column(
        DateTime,
        nullable=False,
        default=func.now(),
        server_default=func.now(),
        onupdate=func.now(),
    )

    @staticmethod
    def make_password_hash(password):
        hash_ = bcrypt.hashpw(password=password.encode('utf-8'), salt=bcrypt.gensalt())
        return hash_.decode('utf-8')

    def is_password_valid(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
