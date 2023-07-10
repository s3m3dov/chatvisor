import stripe

from core.config import settings
from core.logging import logger
from entities.models import (
    User,
    CustomerSubscription as SubscriptionModel,
)
from entities.schemas import (
    CustomerSubscription as SubscriptionSchema,
)

stripe.api_key = settings.stripe.api_secret_key


class SubscriptionCRUD:
    @staticmethod
    def create_subscription(subscription: SubscriptionSchema):
        user = User.where(customer_id__exact=subscription.customer).first()
        if not user:
            logger.error(f"User not found: {subscription.customer}")
            return

        SubscriptionModel.create(
            id=subscription.id,
            created_at=subscription.created,
            status=subscription.status,
            current_period_start=subscription.current_period_start,
            current_period_end=subscription.current_period_end,
            cancel_at_period_end=subscription.cancel_at_period_end,
            cancel_at=subscription.cancel_at,
            user_id=user.id,
        )

    @classmethod
    def update_subscription(cls, subscription: SubscriptionSchema):
        subscription_model = SubscriptionModel.find(subscription.id)
        if not subscription_model:
            cls.create_subscription(subscription)

        subscription_model.update(
            status=subscription.status,
            current_period_start=subscription.current_period_start,
            current_period_end=subscription.current_period_end,
            cancel_at_period_end=subscription.cancel_at_period_end,
            cancel_at=subscription.cancel_at,
        )
        subscription_model.save()
