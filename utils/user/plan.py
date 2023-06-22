from typing import Optional, Tuple

import pendulum
import stripe
from sqlalchemy import func

from core.config import settings
from core.config.submodels.main import PlanConfig
from core.database import session_scope
from core.logging import logger
from entities.enums import SubscriptionStatus, PlanLimitDuration
from entities.models import CustomerSubscription, PromptMessage
from entities.models import (
    User,
)
from entities.schemas import (
    CheckoutSession,
)

__all__ = ["UserPlan"]
stripe.api_key = settings.stripe.api_secret_key


class UserPlan:
    def __init__(self, user_id: str, channel_id: int) -> None:
        self.user_id = user_id
        self.subscription = self.get_subscription(user_id)
        self.channel_id = channel_id
        self.plan = self.get_current_plan()

    @staticmethod
    def get_subscription(user_id: str) -> CustomerSubscription:
        subscription = CustomerSubscription.smart_query(
            filters={"user_id__exact": user_id},
            sort_attrs=["-updated_at", "-created_at"],
        ).first()
        logger.debug(f"Subscription: {subscription}")
        return subscription

    @property
    def is_premium(self) -> bool:
        if self.subscription:
            logger.debug(f"Subscription status: {self.subscription.status}")
            return SubscriptionStatus.is_active(self.subscription.status)

        return False

    def get_current_plan(self) -> PlanConfig:
        if self.is_premium:
            logger.info(f"User {self.user_id} is premium")
            return settings.premium_plan
        else:
            logger.info(f"User {self.user_id} is basic")
            return settings.basic_plan

    def is_plan_limit_reached(self) -> bool:
        match self.plan.limit_duration:
            case PlanLimitDuration.DAILY:
                return self.is_day_limit_reached()
            case PlanLimitDuration.MONTHLY:
                raise NotImplementedError
            case PlanLimitDuration.LIFETIME:
                return self.is_lifetime_limit_reached()
            case other:
                logger.warning(f"Unknown plan limit duration: {other}")

    def is_day_limit_reached(self) -> bool:
        usage = self.get_daily_usage()
        result = usage >= self.plan.limit_amount
        logger.info(
            "Usage: %s, user: %s, channel: %s, plan: %s, duration: %s, limit: %s, result: %s",
            usage, self.user_id, self.channel_id, self.plan.name, self.plan.limit_duration,
            self.plan.limit_amount, result
        )
        return result

    def is_lifetime_limit_reached(self) -> bool:
        usage = self.get_lifetime_usage()
        result = usage >= self.plan.limit_amount
        logger.info(
            "Usage: %s, user: %s, channel: %s, plan: %s, duration: %s, limit: %s, result: %s",
            usage, self.user_id, self.channel_id, self.plan.name, self.plan.limit_duration,
            self.plan.limit_amount, result
        )
        return result

    def get_daily_usage(self) -> float:
        earlier_by_24h = pendulum.now("UTC").subtract(days=1).int_timestamp
        with session_scope() as session:
            usage = (
                session.query(func.sum(PromptMessage.cost).label("usage"))
                .filter(
                    PromptMessage.channel_id == self.channel_id,
                    PromptMessage.created_at >= earlier_by_24h,
                )
                .scalar()
            )
        return usage or 0

    def get_lifetime_usage(self) -> float:
        with session_scope() as session:
            usage = (
                session.query(func.sum(PromptMessage.cost).label("usage"))
                .filter(PromptMessage.channel_id == self.channel_id)
                .scalar()
            )

        return usage or 0

    def create_checkout_session(
        self, user: User
    ) -> Tuple[bool, Optional[CheckoutSession]]:
        """Get an employee.
        Args:
            user (User): The internal user + stripe customer.

        Returns:
            bool: True if the user is subscribed.
            CheckoutSession: The checkout session if user is not subscribed.
        """
        if self.is_premium:
            return True, None
        else:
            _session = self._create_checkout_session(user=user)
            return False, _session

    @staticmethod
    def _create_checkout_session(user: User) -> CheckoutSession:
        _session: stripe.checkout.Session = stripe.checkout.Session.create(
            customer=user.customer_id,
            metadata={"user_id": user.id},
            mode="subscription",
            payment_method_types=["card"],
            currency=settings.stripe.currency,
            success_url=settings.stripe.success_url,
            phone_number_collection={
                "enabled": settings.stripe.phone_number_collection_enabled,
            },
            line_items=[
                {"price": settings.stripe.price_id, "quantity": 1},
            ],
            subscription_data={
                "trial_settings": {"end_behavior": {"missing_payment_method": "pause"}},
                "trial_period_days": settings.stripe.trial_period_days,
            },
        )
        return CheckoutSession(**_session)
