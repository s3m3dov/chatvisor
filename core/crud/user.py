from typing import Any, Dict, Optional

import stripe

from config import settings
from core.utils.basic import get_full_name
from entities.enums import Platform, SystemUser
from entities.models import (
    UserChannel,
    User,
    PromptMessage,
    OutputMessage,
    Customer as CustomerModel,
    CustomerSubscription as SubscriptionModel,
)
from entities.schemas import (
    Customer as CustomerSchema,
    CustomerSubscription as SubscriptionSchema,
    CheckoutSession
)

stripe.api_key = settings.stripe_secret_key

log = print


def get_user_channel(platform_user_id: int) -> Optional[UserChannel]:
    user_channel = (
        UserChannel.with_joined(UserChannel.user)
        .where(UserChannel.platform_user_id == platform_user_id)
        .first()
    )
    log(f"user_channel: {user_channel}")
    return user_channel


def get_customer(user_id: int) -> Optional[CustomerModel]:
    customer = (
        CustomerModel.with_joined(CustomerModel.user)
        .where(CustomerModel.user_id == user_id)
        .first()
    )
    log(f"customer: {customer}")
    return customer


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
        full_name = get_full_name(
            user_channel.user.first_name, user_channel.user.last_name
        )

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


def create_stripe_customer(user_id: int) -> stripe.Customer:
    customer = stripe.Customer.create(
        metadata={"user_id": user_id},
    )
    return customer


def create_checkout_session(customer_id: str) -> CheckoutSession:
    _session = stripe.checkout.Session.create(
        customer=customer_id,
        payment_method_types=["card"],
        line_items=[
            {"price": settings.stripe_price_id, "quantity": 1},
        ],
        phone_number_collection={
            "enabled": settings.phone_number_collection_enabled,
        },
        currency=settings.currency,
        mode="subscription",
        success_url=settings.stripe_success_url, subscription_data={
            "trial_settings": {"end_behavior": {"missing_payment_method": "pause"}},
            "trial_period_days": settings.trial_period_days,
        },
    )
    session = CheckoutSession(
        **_session
    )

    return session


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
        meta_data=customer.metadata,
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
    customer_model.save()


def create_customer_subscription_model(subscription: SubscriptionSchema):
    customer_model = CustomerModel.find(subscription.customer)
    if not customer_model:
        raise ValueError(f"Customer with id={subscription.customer} not found")

    SubscriptionModel.create(
        id=subscription.id,
        customer_id=subscription.customer,
        created_at=subscription.created,
        status=subscription.status,
        current_period_start=subscription.current_period_start,
        current_period_end=subscription.current_period_end,
        cancel_at_period_end=subscription.cancel_at_period_end,
        cancel_at=subscription.cancel_at,
    )


def update_customer_subscription_model(subscription: SubscriptionSchema):
    subscription_model = SubscriptionModel.find(subscription.id)
    if not subscription_model:
        create_customer_subscription_model(subscription)

    subscription_model.update(
        status=subscription.status,
        current_period_start=subscription.current_period_start,
        current_period_end=subscription.current_period_end,
        cancel_at_period_end=subscription.cancel_at_period_end,
        cancel_at=subscription.cancel_at,
    )
    subscription_model.save()
