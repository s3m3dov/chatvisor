from enum import StrEnum

from .base import BaseEnum


class Platform(StrEnum, BaseEnum):
    TELEGRAM = "telegram"
    DISCORD = "discord"


class SystemUser(StrEnum, BaseEnum):
    SYSTEM = "system"
    GPT_3_5_TURBO = "gpt-3.5 turbo"
    GPT_4 = "gpt-4"
    DALL_E = "dall-e"
