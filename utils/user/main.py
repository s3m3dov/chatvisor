import uuid
from typing import Optional, Tuple
from typing import Union

import stripe

from core.config import settings
from core.logging import logger
from entities.enums import Platform
from entities.models import (
    UserChannel,
    User,
)
from entities.schemas import (
    Customer as CustomerSchema,
    TelegramUser,
)
from utils.user.base import get_full_name

stripe.api_key = settings.stripe.api_secret_key


class UserCRUD:
    @staticmethod
    def _generate_uuid() -> uuid.UUID:
        return uuid.uuid4()

    @staticmethod
    def _create_stripe_customer(user_id: uuid.UUID, full_name: str) -> CustomerSchema:
        _customer: stripe.Customer = stripe.Customer.create(
            name=full_name, metadata={"user_id": user_id}
        )
        customer = CustomerSchema(**_customer)
        return customer

    @classmethod
    def create_user_n_channel(
        cls, platform: Platform, data: Union[TelegramUser]
    ) -> UserChannel:
        unique_id = cls._generate_uuid()
        full_name = get_full_name(data.first_name, data.last_name)
        customer = cls._create_stripe_customer(user_id=unique_id, full_name=full_name)
        user = User.create(
            id=unique_id,
            customer_id=customer.id,
            first_name=data.first_name,
            last_name=data.last_name,
            full_name=full_name,
            meta_data=customer.metadata,
            email=customer.email,
            phone=customer.phone,
        )
        user_channel = UserChannel.create(
            platform=platform,
            platform_user_id=data.id,
            user_id=user.id,
            data=data.optional_data.dict(),
        )
        return user_channel

    @staticmethod
    def update_user_via_stripe(customer: CustomerSchema) -> User:
        user_id = customer.metadata.get("user_id")
        if not user_id:
            raise ValueError("user_id not found in customer metadata")

        user = User.find_or_fail(user_id)
        user.update(
            email=customer.email,
            phone=customer.phone,
            full_name=customer.name,
        )
        user.save()
        return user


def get_or_create_user_channel(
    platform: Platform, data: Union[TelegramUser]
) -> Tuple[bool, Optional[UserChannel]]:
    platform_user_id = data.id
    logger.info(f"getting user channel: platform_user_id: {platform_user_id}")
    user_channel = (
        UserChannel.with_joined(UserChannel.user)
        .where(UserChannel.platform_user_id == platform_user_id)
        .first()
    )

    if not user_channel:
        user_channel = UserCRUD.create_user_n_channel(platform=platform, data=data)
        logger.info(
            f"User channel created: {user_channel.id} "
            f"platform_id: {platform_user_id} "
            f"user: {user_channel.user}"
        )
        is_created = True
    else:
        is_created = False

    logger.info(f"user_channel: {user_channel}")
    return is_created, user_channel
