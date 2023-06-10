from dotenv import dotenv_values
from pydantic import BaseSettings

from core.config.submodels.main import (
    LLMConfig,
    TelegramConfig,
    SlackConfig,
    StripeConfig,
    PlanConfig,
)
from entities.enums import SystemUser, Plan, PlanLimitDuration

config = dotenv_values(".env")


class Config(BaseSettings):
    """Config class for settings."""

    openapi_key: str = config["OPENAI_API_KEY"]
    db_url: str = config["DATABASE_URL"]

    telegram: TelegramConfig = TelegramConfig(
        bot_token=config["TELEGRAM_BOT_TOKEN"],
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
    basic_plan: PlanConfig = PlanConfig(
        name=Plan.BASIC,
        limit_amount=0.1,
        limit_duration=PlanLimitDuration.LIFETIME,
    )
    premium_plan: PlanConfig = PlanConfig(
        name=Plan.PREMIUM,
        limit_amount=1,
        limit_duration=PlanLimitDuration.DAILY,
    )
    slack: SlackConfig = SlackConfig(
        token=config["SLACK_TOKEN"],
        channel=config["SLACK_CHANNEL"],
        icon_url=config.get("SLACK_ICON_URL"),
    )
    stripe: StripeConfig = StripeConfig(
        api_pub_key=config["STRIPE_API_PUBLISHABLE_KEY"],
        api_secret_key=config["STRIPE_API_SECRET_KEY"],
        webhook_secret=config["STRIPE_WEBHOOK_SECRET"],
        success_url=config["STRIPE_SUCCESS_URL"],
        dashboard_url=config["STRIPE_DASHBOARD_URL"],
        price_id=config["STRIPE_PRICE_ID"],
        trial_period_days=config["STRIPE_TRIAL_PERIOD_DAYS"],
    )
