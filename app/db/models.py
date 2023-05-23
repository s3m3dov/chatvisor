from typing import Optional, List

from pgvector.sqlalchemy import Vector
from sqlalchemy import (Integer, String, ForeignKey)
from sqlalchemy.orm import (
    DeclarativeBase,
    relationship,
    Mapped,
    mapped_column
)
from sqlalchemy_utils import ChoiceType

from app.db.enums import Platform, SystemUser


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    channels: Mapped[List["UserChannel"]] = relationship(back_populates="user")

    @property
    def full_name(self) -> str:
        return (
            " ".join([self.first_name, self.last_name])
            if self.last_name
            else self.first_name
        )

    def __str__(self) -> str:
        return self.full_name


class UserChannel(Base):
    __tablename__ = "users_channels"

    id: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True)
    platform: Mapped[Platform] = mapped_column(ChoiceType(Platform, impl=Integer()), nullable=False)
    platform_chat_id: Mapped[int] = mapped_column(Integer, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)

    user: Mapped["User"] = relationship(back_populates="user_channels")

    def __str__(self) -> str:
        return f"{self.platform.name}: {self.platform_chat_id}"


class PromptMessage(Base):
    __tablename__ = "prompt_messages"

    id: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True)
    text: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    text_embedding: Mapped[Optional[Vector]] = mapped_column(Vector, nullable=True)

    channel_id: Mapped[int] = mapped_column(Integer, ForeignKey("users_channels.id"), nullable=False)
    sender_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)

    channel: Mapped["UserChannel"] = relationship(back_populates="messages")
    sender: Mapped["User"] = relationship(back_populates="messages")
    output: Mapped["OutputMessage"] = relationship(back_populates="prompt")


class OutputMessage(Base):
    __tablename__ = "output_messages"

    id: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True)
    text: Mapped[Optional[Vector]] = mapped_column(Vector, nullable=True)
    text_embedding: Mapped[Optional[Vector]] = mapped_column(String, nullable=True)

    sender_id: Mapped[SystemUser] = mapped_column(ChoiceType(SystemUser, impl=Integer()), nullable=False)
    prompt_id: Mapped[int] = mapped_column(Integer, ForeignKey("users_messages.id"), nullable=False)

    prompt: Mapped["PromptMessage"] = relationship(back_populates="output")
