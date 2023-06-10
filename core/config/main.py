from dotenv import dotenv_values
from pydantic import BaseSettings

from core.config.submodels.main import (
    LLMConfig,
    TelegramConfig,
    DBConfig,
    StripeConfig,
    PlanConfig,
)
from entities.enums import SystemUser, Plan, PlanLimitDuration

config = dotenv_values(".env")


class Config(BaseSettings):
    """Config class for settings."""
    openapi_key: str = config["OPENAI_API_KEY"]
    slack_icon_url: str = "https://avatars.slack-edge.com/2023-06-09/5426672302464_1bddaa605d4fe61b6cc0_512.png"
    slack_token: str = config["SLACK_API_TOKEN"]
    slack_channel: str = config["SLACK_CHANNEL"]

    telegram: TelegramConfig = TelegramConfig(
        bot_token=config["TELEGRAM_BOT_TOKEN"],
    )
    db: DBConfig = DBConfig(
        driver=config["DB_DRIVER"],
        user=config["DB_USER"],
        password=config["DB_PASSWORD"],
        host=config["DB_HOST"],
        port=config["DB_PORT"],
        database=config["DB_DATABASE"],
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
    stripe: StripeConfig = StripeConfig(
        api_pub_key=config["STRIPE_API_PUBLISHABLE_KEY"],
        api_secret_key=config["STRIPE_API_SECRET_KEY"],
        webhook_secret=config["STRIPE_WEBHOOK_SECRET"],
        success_url="https://s3m3dov.github.io/simple-success-page/",
        dashboard_url="https://billing.stripe.com/p/login/test_14kfZT5bre7ubO8fYY",
        price_id="price_1NAWLbHCGQv2kDWZu8N1uuOO",
        trial_period_days=1,
    )
