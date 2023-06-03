import uuid
from typing import Optional, Tuple
from typing import Union

import stripe

from config import settings
from core.user.base import get_full_name
from entities.enums import Platform
from entities.models import (
    User,
)
from entities.models import (
    UserChannel,
)
from entities.schemas import (
    Customer as CustomerSchema,
    TelegramUser,
)

stripe.api_key = settings.stripe.api_secret_key

log = print


class UserCRUD:
    @staticmethod
    def _generate_uuid() -> uuid.UUID:
        return uuid.uuid4()

    @staticmethod
    def _create_stripe_customer(user_id: uuid.UUID) -> CustomerSchema:
        _customer: stripe.Customer = stripe.Customer.create(
            metadata={"user_id": user_id}
        )
        customer = CustomerSchema(**_customer)
        return customer

    @classmethod
    def create_user(cls, platform: Platform, data: Union[TelegramUser]):
        unique_id = cls._generate_uuid()
        customer = cls._create_stripe_customer(user_id=unique_id)
        user = User.create(
            id=unique_id,
            customer_id=customer.id,
            first_name=data.first_name,
            last_name=data.last_name,
            full_name=get_full_name(data.first_name, data.last_name),
            meta_data=customer.metadata,
            email=customer.email,
            phone=customer.phone,
        )
        log(f"user created: {user}")
        UserChannel.create(
            platform=platform,
            platform_user_id=data.id,
            user_id=user.id,
            data=data.optional_data.dict(),
        )
        return user

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


def get_user_channel(platform_user_id: int) -> Optional[UserChannel]:
    user_channel = (
        UserChannel.with_joined(UserChannel.user)
        .where(UserChannel.platform_user_id == platform_user_id)
        .first()
    )
    log(f"user_channel: {user_channel}")
    return user_channel


def get_or_create_user(
    platform: Platform,
    data: Union[TelegramUser],
) -> Tuple[bool, User]:
    user_channel = get_user_channel(platform_user_id=data.id)

    if not user_channel:
        user = UserCRUD.create_user(platform=platform, data=data)
        is_created = True
    else:
        user = user_channel.user
        is_created = False

    return is_created, user
