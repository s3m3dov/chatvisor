from typing import Any, Dict, Optional

from stripe import Customer as StripeCustomer

from core.utils.basic import get_full_name
from entities.enums import Platform, SystemUser
from entities.models import UserChannel, User, PromptMessage, OutputMessage, Customer as CustomerModel
from entities import Customer as CustomerSchema

log = print


def get_user_channel(platform_user_id: int) -> Optional[UserChannel]:
    user_channel = (
        UserChannel.with_joined(UserChannel.user)
        .where(UserChannel.platform_user_id == platform_user_id)
        .first()
    )
    log(f"user_channel: {user_channel}")
    return user_channel


def get_or_create_user(
        platform_user_id: int,
        first_name: str,
        last_name: str,
        data: Dict[str, Any],
) -> Dict[str, Any]:
    user_channel = get_user_channel(platform_user_id=platform_user_id)

    if not user_channel:
        user = User.create(
            first_name=first_name,
            last_name=last_name,
        )
        log(f"user created: {user}")
        UserChannel.create(
            platform=Platform.TELEGRAM,
            platform_user_id=platform_user_id,
            user_id=user.id,
            data=data,
        )
        create_stripe_customer(user_id=user.id)

        is_created = True
        full_name = get_full_name(first_name, last_name)
    else:
        is_created = False
        full_name = get_full_name(user_channel.user.first_name, user_channel.user.last_name)

    return {
        "is_created": is_created,
        "full_name": full_name,
    }


def save_prompt_n_output(
        platform_user_id: int, prompt: str, output: str, system_sender: SystemUser
) -> None:
    user_channel = get_user_channel(platform_user_id=platform_user_id)
    prompt_message = PromptMessage.create(
        text=prompt,
        sender_id=user_channel.user_id,
        channel_id=user_channel.id,
    )
    log(f"PromptMessage created: {prompt_message}")
    output_message = OutputMessage.create(
        text=output,
        prompt_id=prompt_message.id,
        sender_id=system_sender,
    )
    log(f"OutputMessage created: {output_message}")


def create_stripe_customer(user_id: int) -> StripeCustomer:
    customer = StripeCustomer.create(
        metadata={"user_id": user_id},
    )
    return customer


def create_customer_model(customer: CustomerSchema):
    user_id = customer.metadata.get("user_id")
    if not user_id:
        raise ValueError("user_id not found in customer metadata")

    CustomerModel.create(
        id=customer.id,
        user_id=user_id,
        full_name=customer.name,
        email=customer.email,
        phone=customer.phone,
        metadata=customer.metadata,
        created_at=customer.created,
    )


def update_customer_model(customer: CustomerSchema):
    user_id = customer.metadata.get("user_id")
    if not user_id:
        raise ValueError("user_id not found in customer metadata")

    customer_model = CustomerModel.find(customer.id)
    if not customer_model:
        raise ValueError(f"Customer with id={customer.id} not found")

    customer_model.update(
        full_name=customer.name,
        email=customer.email,
        phone=customer.phone,
    )
