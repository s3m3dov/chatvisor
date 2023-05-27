from typing import Optional, List

from sqlalchemy import (Integer, String, JSON, ForeignKey)
from sqlalchemy.orm import (
    relationship,
    Mapped,
    mapped_column
)
from sqlalchemy.types import Enum as saEnum

from core.entities.enums import Platform, SystemUser
from .base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True, nullable=False, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    channels: Mapped[List["UserChannel"]] = relationship(back_populates="user")
    prompts: Mapped[List["PromptMessage"]] = relationship(back_populates="sender")

    def __str__(self) -> str:
        return (
            " ".join([self.first_name, self.last_name])
            if self.last_name
            else self.first_name
        )


class UserChannel(Base):
    __tablename__ = "users_channels"

    id: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True, nullable=False, autoincrement=True)
    platform: Mapped[Platform] = mapped_column(saEnum(Platform, name="platform"), nullable=False)
    platform_user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    data: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey(User.id), nullable=False)

    user: Mapped["User"] = relationship(back_populates="channels")
    prompts: Mapped[List["PromptMessage"]] = relationship(back_populates="channel")

    def __str__(self) -> str:
        return f"{self.platform.name}: {self.platform_user_id}"


class PromptMessage(Base):
    __tablename__ = "prompt_messages"

    id: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True, nullable=False, autoincrement=True)
    text: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    # embedding: Mapped[Optional[Vector]] = mapped_column(Vector, nullable=True)

    channel_id: Mapped[int] = mapped_column(Integer, ForeignKey(UserChannel.id), nullable=False)
    sender_id: Mapped[int] = mapped_column(Integer, ForeignKey(User.id), nullable=False)

    channel: Mapped["UserChannel"] = relationship(back_populates="prompts")
    sender: Mapped["User"] = relationship(back_populates="prompts")
    output: Mapped["OutputMessage"] = relationship(back_populates="prompt")


class OutputMessage(Base):
    __tablename__ = "output_messages"

    id: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True, nullable=False, autoincrement=True)
    text: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    # embedding: Mapped[Optional[Vector]] = mapped_column(Vector, nullable=True)

    sender_id: Mapped[SystemUser] = mapped_column(saEnum(SystemUser, name="system_user"), nullable=False)
    prompt_id: Mapped[int] = mapped_column(Integer, ForeignKey(PromptMessage.id), nullable=False)

    prompt: Mapped["PromptMessage"] = relationship(back_populates="output")
