from typing import Optional, Tuple

import stripe

from core.config import settings
from entities.models import (
    User,
)
from entities.schemas import (
    CheckoutSession,
)
from .base import is_user_subscribed

stripe.api_key = settings.stripe.api_secret_key

log = print

__all__ = ["CheckoutSessionCRUD"]


class CheckoutSessionCRUD:
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
        session = CheckoutSession(**_session)

        return session

    @classmethod
    def create_checkout_session(
        cls, user: User
    ) -> Tuple[bool, Optional[CheckoutSession]]:
        """Get an employee.
        Args:
            user: User: The internal user + stripe customer.

        Returns:
            bool: True if the user is subscribed.
            CheckoutSession: The checkout session if user is not subscribed.
        """
        if is_user_subscribed(user_id=user.id):
            return True, None
        else:
            session = cls._create_checkout_session(user=user)
            return False, session
