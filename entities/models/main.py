from typing import Optional, List

from sqlalchemy import (Integer, String, Boolean, JSON, ForeignKey)
from sqlalchemy.orm import (
    relationship,
    Mapped,
    mapped_column
)
from sqlalchemy.types import Enum as saEnum

from core.entities.enums import Platform, SystemUser
from .base import BaseModel


class User(BaseModel):
    __tablename__ = "users"
    __repr_attrs__ = ["id", "first_name", "last_name"]

    id: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True, nullable=False, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    channels: Mapped[List["UserChannel"]] = relationship(back_populates="user")
    prompts: Mapped[List["PromptMessage"]] = relationship(back_populates="sender")
    customer: Mapped["Customer"] = relationship("Customer", uselist=False, back_populates="user")
    customer_subscriptions: Mapped[List["CustomerSubscription"]] = relationship("CustomerSubscription",
                                                                                back_populates="user")

    def __str__(self) -> str:
        return (
            " ".join([self.first_name, self.last_name])
            if self.last_name
            else self.first_name
        )


class UserChannel(BaseModel):
    __tablename__ = "users_channels"
    __repr_attrs__ = ["id", "platform", "platform_user_id"]

    id: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True, nullable=False, autoincrement=True)
    platform: Mapped[Platform] = mapped_column(saEnum(Platform, name="platform"), nullable=False)
    platform_user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    data: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey(User.id), nullable=False)

    user: Mapped["User"] = relationship(back_populates="channels")
    prompts: Mapped[List["PromptMessage"]] = relationship(back_populates="channel")

    def __str__(self) -> str:
        return f"{self.platform.name}: {self.platform_user_id}"


class PromptMessage(BaseModel):
    __tablename__ = "prompt_messages"
    __repr_attrs__ = ["id", "text", "sender_id", "channel_id"]

    id: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True, nullable=False, autoincrement=True)
    text: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    # openai_embedding: Mapped[Optional[Vector]] = mapped_column(Vector, nullable=True)

    channel_id: Mapped[int] = mapped_column(Integer, ForeignKey(UserChannel.id), nullable=False)
    sender_id: Mapped[int] = mapped_column(Integer, ForeignKey(User.id), nullable=False)

    channel: Mapped["UserChannel"] = relationship(back_populates="prompts")
    sender: Mapped["User"] = relationship(back_populates="prompts")
    output: Mapped["OutputMessage"] = relationship(back_populates="prompt")


class OutputMessage(BaseModel):
    __tablename__ = "output_messages"
    __repr_attrs__ = ["id", "text", "sender_id"]

    id: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True, nullable=False, autoincrement=True)
    text: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    # openai_embedding: Mapped[Optional[Vector]] = mapped_column(Vector, nullable=True)

    sender_id: Mapped[SystemUser] = mapped_column(saEnum(SystemUser, name="system_user"), nullable=False)
    prompt_id: Mapped[int] = mapped_column(Integer, ForeignKey(PromptMessage.id), nullable=False)

    prompt: Mapped["PromptMessage"] = relationship(back_populates="output")


class Customer(BaseModel):
    """
    Customer model;
    data provided by Stripe.
    """
    __tablename__ = "customers"
    __repr_attrs__ = ["id", "full_name", "email"]

    id: Mapped[str] = mapped_column(Integer, primary_key=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String, nullable=True)
    email: Mapped[str] = mapped_column(String, nullable=False)
    phone: Mapped[str] = mapped_column(String, nullable=True)
    meta_data: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    created_at: Mapped[int] = mapped_column(Integer, nullable=False)

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey(User.id), nullable=True)

    user: Mapped["User"] = relationship(back_populates="customer")


class CustomerSubscription(BaseModel):
    """
    Customer subscription model;
    data provided by Stripe.
    """
    __tablename__ = "customer_subscriptions"
    __repr_attrs__ = ["id", "customer_id", "status"]

    id: Mapped[str] = mapped_column(String, primary_key=True, nullable=False)
    customer_id: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)
    current_period_start: Mapped[int] = mapped_column(Integer, nullable=False)
    current_period_end: Mapped[int] = mapped_column(Integer, nullable=False)
    cancel_at_period_end: Mapped[bool] = mapped_column(Boolean, nullable=False)
    started_at: Mapped[int] = mapped_column(Integer, nullable=False)
    cancel_at: Mapped[int] = mapped_column(Integer, nullable=True)

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey(User.id), nullable=True)

    user: Mapped["User"] = relationship(back_populates="customer_subscriptions")
