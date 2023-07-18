from environs import Env
from pydantic import BaseSettings

from core.config.submodels.main import (
    LLMConfig,
    ImageGenConfig,
    TelegramConfig,
    SlackConfig,
    StripeConfig,
    PlanConfig,
)
from entities.enums import SystemUser, Plan, PlanLimitDuration

env = Env()
env.read_env()


class Config(BaseSettings):
    """Config class for settings."""

    openapi_key: str = env("OPENAI_API_KEY")
    db_url: str = env("DATABASE_URL")
    limit: int = env.int("LIMIT", default=10)
    telegram: TelegramConfig = TelegramConfig(
        bot_token=env("TELEGRAM_BOT_TOKEN"),
    )
    gpt3_5_turbo: LLMConfig = LLMConfig(
        name=SystemUser.GPT_3_5_TURBO,
        temperature=0.3,
        max_tokens=300,
    )
    gpt4: LLMConfig = LLMConfig(
        name=SystemUser.GPT_4,
        temperature=0.3,
        max_tokens=450,
    )
    dalle: ImageGenConfig = ImageGenConfig(
        name=SystemUser.DALL_E,
        resolution="1024x1024",
        price=0.020
    )
    basic_plan: PlanConfig = PlanConfig(
        name=Plan.BASIC,
        limit_amount=0.1,
        limit_duration=PlanLimitDuration.LIFETIME,
    )
    premium_plan: PlanConfig = PlanConfig(
        name=Plan.PREMIUM,
        limit_amount=8,
        limit_duration=PlanLimitDuration.MONTHLY,
    )
    slack: SlackConfig = SlackConfig(
        token=env("SLACK_TOKEN"),
        channel=env("SLACK_CHANNEL"),
        icon_url=env("SLACK_ICON_URL", None),
    )
    stripe: StripeConfig = StripeConfig(
        api_pub_key=env("STRIPE_API_PUBLISHABLE_KEY"),
        api_secret_key=env("STRIPE_API_SECRET_KEY"),
        webhook_secret=env("STRIPE_WEBHOOK_SECRET"),
        success_url=env("STRIPE_SUCCESS_URL"),
        dashboard_url=env("STRIPE_DASHBOARD_URL"),
        price_id=env("STRIPE_PRICE_ID"),
        trial_period_days=env.int("STRIPE_TRIAL_PERIOD_DAYS"),
    )
