import stripe

from core.config import settings
from core.database import session_scope
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
        with session_scope() as session:
            user = (
                session.query(User)
                .filter(User.customer_id == subscription.customer)
                .first()
            )
            if not user:
                logger.error(f"User not found: {subscription.customer}")
                return

            subscription_model = SubscriptionModel(
                id=subscription.id,
                created_at=subscription.created,
                status=subscription.status,
                current_period_start=subscription.current_period_start,
                current_period_end=subscription.current_period_end,
                cancel_at_period_end=subscription.cancel_at_period_end,
                cancel_at=subscription.cancel_at,
                user_id=user.id,
            )
            session.add(subscription_model)

    @classmethod
    def update_subscription(cls, subscription: SubscriptionSchema):
        with session_scope() as session:
            subscription_model = session.query(SubscriptionModel).filter(
                SubscriptionModel.id == subscription.id
            )
            if not subscription_model:
                logger.error(f"Subscription not found: {subscription.id}")
                return
            subscription_model.update(
                dict(
                    status=subscription.status,
                    current_period_start=subscription.current_period_start,
                    current_period_end=subscription.current_period_end,
                    cancel_at_period_end=subscription.cancel_at_period_end,
                    cancel_at=subscription.cancel_at,
                )
            )
