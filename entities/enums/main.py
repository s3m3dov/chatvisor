from enum import StrEnum

from .base import BaseEnum


class Platform(StrEnum, BaseEnum):
    TELEGRAM = "telegram"
    DISCORD = "discord"


class SystemUser(StrEnum, BaseEnum):
    SYSTEM = "system"
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    GPT_4 = "gpt-4"
    DALL_E = "dall-e"


class PlanLimitDuration(StrEnum, BaseEnum):
    LIFETIME = "lifetime"
    DAILY = "daily"
    MONTHLY = "monthly"


class Plan(StrEnum, BaseEnum):
    BASIC = "basic"
    PREMIUM = "premium"


class SubscriptionStatus(StrEnum, BaseEnum):
    """
    Possible values are incomplete, incomplete_expired, trialing, active, past_due,
    canceled, or unpaid.
    https://stripe.com/docs/api/subscriptions/object#subscription_object-status
    """

    ACTIVE = "active"
    TRIALING = "trialing"
    INCOMPLETE = "incomplete"
    INCOMPLETE_EXPIRED = "incomplete_expired"
    PAST_DUE = "past_due"
    CANCELED = "canceled"
    UNPAID = "unpaid"

    @classmethod
    def is_active(cls, status: str) -> bool:
        return status in [cls.ACTIVE.value, cls.TRIALING.value]
