from typing import Optional

from pydantic.class_validators import validator
from pydantic.main import BaseModel
from telegram.constants import ChatType

__all__ = ["TelegramUser"]


class TelegramChat(BaseModel):
    id: int
    type: ChatType
    title: Optional[str] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    bio: Optional[str] = None
    description: Optional[str] = None

    @validator("type")
    def validate_chat_type(cls, v):
        if v not in ChatType.__members__.values():
            raise ValueError(f"Invalid chat type: {v}")
        return v.value


class TelegramOptionalData(BaseModel):
    language_code: Optional[str] = None
    chat: Optional[TelegramChat]


class TelegramUser(BaseModel):
    id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    is_bot: Optional[bool] = False
    optional_data: Optional[TelegramOptionalData]
