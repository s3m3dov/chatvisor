from functools import lru_cache
from typing import Optional

from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, Integer
from sqlalchemy_utils import ChoiceType
from sqlmodel import Field, SQLModel

from .custom_fields import IntPrimaryKey
from .enums import Platform, SystemUser


class User(SQLModel, table=True):
    id: Optional[int] = IntPrimaryKey
    first_name: str = Field(nullable=False)
    last_name: Optional[str]

    __tablename__ = "users"

    @property
    def full_name(self) -> str:
        return (
            " ".join([self.first_name, self.last_name])
            if self.last_name
            else self.first_name
        )

    def __str__(self) -> str:
        return self.full_name

    @lru_cache(maxsize=len(SystemUser))
    def get_system_user(self, system_user: SystemUser):
        pass


class UserChannel(SQLModel, table=True):
    id: Optional[int] = IntPrimaryKey
    external_id: Optional[int] = Field(default=None, nullable=True)
    platform: Platform = Field(
        sa_column=Column(ChoiceType(Platform), impl=Integer()), nullable=False
    )
    user_id: int = Field(default=None, foreign_key=User.id, nullable=False)

    __tablename__ = "users_channels"

    def __str__(self) -> str:
        return f"{self.platform.name}: {self.external_id}"


class Message(SQLModel, table=True):
    id: Optional[int] = IntPrimaryKey
    text: Optional[str] = Field(default=None, nullable=True)
    text_embedding: Optional[str] = Field(
        default=None,
        index=True,
        nullable=True,
        sa_column=Column(Vector),
    )
    channel_id: int = Field(default=None, foreign_key=UserChannel.id, nullable=False)
    sender_id: int = Field(default=None, foreign_key=User.id, nullable=False)

    __tablename__ = "messages"

    def __str__(self) -> str:
        return f"{self.text}"
