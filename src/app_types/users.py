from enum import Enum


class MyEnum(Enum):

    @classmethod
    def list(cls):
        return list(map(lambda c: c.name, cls))


class UserType(MyEnum):
    ADMIN = 1
    USER = 2
    EXTERNAL_SYSTEM = 3
