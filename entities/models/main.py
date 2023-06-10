import uuid
from typing import Optional, List

import pendulum
from pgvector.sqlalchemy import Vector
from sqlalchemy import Integer, String, Boolean, JSON, ForeignKey, UUID, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.types import Enum as saEnum

from entities.enums import Platform, SystemUser
from .base import BaseModel


class User(BaseModel):
    __tablename__ = "users"
    __repr_attrs__ = ["id", "first_name", "last_name", "full_name"]

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, nullable=False)
    customer_id: Mapped[str] = mapped_column(
        String, nullable=False
    )  # Customer ID in Stripe

    created_at: Mapped[int] = mapped_column(
        Integer, nullable=False, default=pendulum.now("UTC").int_timestamp
    )
    updated_at: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=pendulum.now("UTC").int_timestamp,
        onupdate=pendulum.now("UTC").int_timestamp,
    )

    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    full_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    email: Mapped[str] = mapped_column(String, nullable=True)
    phone: Mapped[str] = mapped_column(String, nullable=True)
    meta_data: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    channels: Mapped[List["UserChannel"]] = relationship(back_populates="user")
    prompts: Mapped[List["PromptMessage"]] = relationship(back_populates="sender")
    customer_subscriptions: Mapped[List["CustomerSubscription"]] = relationship(
        "CustomerSubscription", back_populates="user"
    )


class UserChannel(BaseModel):
    __tablename__ = "users_channels"
    __repr_attrs__ = ["id", "platform", "platform_user_id"]

    id: Mapped[Optional[int]] = mapped_column(
        Integer, primary_key=True, nullable=False, autoincrement=True
    )
    platform: Mapped[Platform] = mapped_column(
        saEnum(Platform, name="platform"), nullable=False
    )
    platform_user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    data: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID, ForeignKey(User.id), nullable=False
    )

    user: Mapped["User"] = relationship(back_populates="channels")
    prompts: Mapped[List["PromptMessage"]] = relationship(back_populates="channel")

    def __str__(self) -> str:
        return f"{self.platform.name}: {self.platform_user_id}"


class PromptMessage(BaseModel):
    __tablename__ = "prompt_messages"
    __repr_attrs__ = ["id", "text", "sender_id", "channel_id"]

    id: Mapped[Optional[int]] = mapped_column(
        Integer, primary_key=True, nullable=False, autoincrement=True
    )
    text: Mapped[Optional[str]] = mapped_column(String, nullable=False)
    prompt_tokens: Mapped[Optional[int]] = mapped_column(Integer, nullable=False)
    completion_tokens: Mapped[Optional[int]] = mapped_column(Integer, nullable=False)
    cost: Mapped[Optional[float]] = mapped_column(
        Float(precision=8), nullable=False
    )  # in USD
    openai_embedding: Mapped[Optional[Vector]] = mapped_column(Vector, nullable=True)
    created_at: Mapped[int] = mapped_column(
        Integer, nullable=False, default=pendulum.now("UTC").int_timestamp
    )

    channel_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(UserChannel.id), nullable=False
    )
    sender_id: Mapped[uuid.UUID] = mapped_column(
        UUID, ForeignKey(User.id), nullable=False
    )
    receiver_id: Mapped[SystemUser] = mapped_column(
        saEnum(SystemUser, name="system_user"), nullable=False
    )

    channel: Mapped["UserChannel"] = relationship(back_populates="prompts")
    sender: Mapped["User"] = relationship(back_populates="prompts")
    output: Mapped["OutputMessage"] = relationship(back_populates="prompt")


class OutputMessage(BaseModel):
    __tablename__ = "output_messages"
    __repr_attrs__ = ["id", "text", "sender_id"]

    id: Mapped[Optional[int]] = mapped_column(
        Integer, primary_key=True, nullable=False, autoincrement=True
    )
    text: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    openai_embedding: Mapped[Optional[Vector]] = mapped_column(Vector, nullable=True)
    created_at: Mapped[int] = mapped_column(
        Integer, nullable=False, default=pendulum.now("UTC").int_timestamp
    )

    prompt_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(PromptMessage.id), nullable=False
    )

    prompt: Mapped["PromptMessage"] = relationship(back_populates="output")


class CustomerSubscription(BaseModel):
    """
    Customer subscription model;
    data provided by Stripe.
    """

    __tablename__ = "customer_subscriptions"
    __repr_attrs__ = ["id", "status"]

    id: Mapped[str] = mapped_column(String, primary_key=True, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[int] = mapped_column(
        Integer, nullable=False
    )  # Customer `created_at` in Stripe
    updated_at: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=pendulum.now("UTC").int_timestamp,
        onupdate=pendulum.now("UTC").int_timestamp,
    )

    current_period_start: Mapped[int] = mapped_column(Integer, nullable=False)
    current_period_end: Mapped[int] = mapped_column(Integer, nullable=False)
    cancel_at_period_end: Mapped[bool] = mapped_column(Boolean, nullable=False)
    cancel_at: Mapped[int] = mapped_column(Integer, nullable=True)

    user_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey(User.id), nullable=True)

    user: Mapped["User"] = relationship(back_populates="customer_subscriptions")
