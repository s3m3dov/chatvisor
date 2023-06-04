from dotenv import dotenv_values
from pydantic import BaseSettings

from entities.config_schemas.main import LLMConfig, TelegramConfig, DBConfig, StripeConfig
from entities.enums import SystemUser

config = dotenv_values(".env")


class Config(BaseSettings):
    """Config class for settings."""
    openapi_key: str = config["OPENAI_API_KEY"]

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
    gpt4: LLMConfig = LLMConfig(
        name=SystemUser.GPT_4,
        temperature=0.3,
        max_tokens=300,
        free_tokens=2000,
        paid_tokens_per_day=10000,
    )
    gpt3_5_turbo: LLMConfig = LLMConfig(
        name=SystemUser.GPT_3_5_TURBO,
        temperature=0.3,
        max_tokens=300,
        free_tokens=2000,
        paid_tokens_per_day=10000,
    )
    stripe: StripeConfig = StripeConfig(
        api_pub_key=config["STRIPE_API_PUBLISHABLE_KEY"],
        api_secret_key=config["STRIPE_API_SECRET_KEY"],
        webhook_secret=config["STRIPE_WEBHOOK_SECRET"],
        success_url="https://s3m3dov.github.io/simple-success-page/",
        dashboard_url="https://billing.stripe.com/p/login/test_14kfZT5bre7ubO8fYY",
        price_id="price_1NAWLbHCGQv2kDWZu8N1uuOO",
        trial_period_days=2,
    )
