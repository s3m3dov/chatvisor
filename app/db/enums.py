from enum import IntEnum


class Platform(IntEnum):
    telegram = 1
    discord = 2

    @classmethod
    def values(cls) -> tuple:
        return tuple(map(lambda c: c.value, cls))


class SystemUser(IntEnum):
    system = 1
    gpt_3_5 = 2
    gpt_4 = 3
    dall_e = 4

    def __str__(self) -> str:
        return self.name.replace("_", " ").title()
