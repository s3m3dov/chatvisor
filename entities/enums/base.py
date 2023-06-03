from enum import Enum


class BaseEnum(Enum):
    @classmethod
    def values(cls) -> tuple:
        return tuple(map(lambda c: c.value, cls))
