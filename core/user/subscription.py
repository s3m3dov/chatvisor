import stripe

from config import settings
from entities.models import (
    User,
    CustomerSubscription as SubscriptionModel,
)
from entities.schemas import (
    CustomerSubscription as SubscriptionSchema,
)

stripe.api_key = settings.stripe_secret_key

log = print


class SubscriptionCRUD:
    @staticmethod
    def create_subscription(subscription: SubscriptionSchema):
        user_id = subscription.metadata.get("user_id")
        log(f"user_id: {user_id}")
        user = User.find_or_fail(user_id)

        SubscriptionModel.create(
            id=subscription.id,
            customer_id=subscription.customer,
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
