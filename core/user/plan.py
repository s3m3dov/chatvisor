from typing import Optional

import pendulum
from sqlalchemy import func

from config import settings
from core.database import session
from entities.config_schemas.main import PlanConfig
from entities.enums import SubscriptionStatus, PlanLimitDuration
from entities.models import CustomerSubscription, PromptMessage

log = print


class PlanLogic:
    def __init__(self, user_id: str, channel_id: int) -> None:
        self.user_id = user_id
        self.channel_id = channel_id
        self.plan = self.get_current_plan()

    @staticmethod
    def get_subscription(user_id: str) -> CustomerSubscription:
        subscription = CustomerSubscription.smart_query(
            filters={"user_id__exact": user_id},
            sort_attrs=["-updated_at", "-created_at"],
        ).first()
        log(f"Subscription: {subscription}")
        return subscription

    @staticmethod
    def is_premium(subscription: Optional[CustomerSubscription]) -> bool:
        if subscription:
            log(f"Subscription status: {subscription.status}")
            return SubscriptionStatus.is_active(subscription.status)

        return False

    def get_current_plan(self) -> PlanConfig:
        subscription = self.get_subscription(self.user_id)
        if self.is_premium(subscription):
            return settings.premium_plan
        else:
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
                log(f"Unknown plan limit duration: {other}")

    def is_day_limit_reached(self) -> bool:
        usage = self.get_daily_usage()
        result = usage >= self.plan.limit_amount
        log(f"Usage: {usage}, plan: {self.plan.name}, limit: {self.plan.limit_amount}, result: {result}")
        return result

    def is_lifetime_limit_reached(self) -> bool:
        usage = self.get_lifetime_usage()
        result = usage >= self.plan.limit_amount
        log(f"Usage: {usage}, plan: {self.plan.name}, limit: {self.plan.limit_amount}, result: {result}")
        return result

    def get_daily_usage(self) -> float:
        earlier_by_24h = pendulum.now("UTC").subtract(days=1).int_timestamp
        usage = (
            session.query(func.sum(PromptMessage.cost).label("usage"))
            .filter(
                PromptMessage.channel_id == self.channel_id,
                PromptMessage.created_at >= earlier_by_24h,
            )
            .scalar()
        )
        return usage

    def get_lifetime_usage(self) -> float:
        usage = (
            session.query(func.sum(PromptMessage.cost).label("usage"))
            .filter(PromptMessage.channel_id == self.channel_id)
            .scalar()
        )
        return usage
