from dotenv import dotenv_values

from pydantic import BaseSettings

config = dotenv_values(".env")


class Config(BaseSettings):
    """Config class for settings."""
    max_tokens = {
        "default": 300,
        "gpt-3": 300,
        "gpt-3.5": 300,
        "gpt-3.5-turbo": 300,
        "gpt-4": 300,
        "dall-e": 300,
    }
    temperature = {
        "default": 0.3,
        "gpt-3": 0.3,
        "gpt-3.5": 0.3,
        "gpt-3.5-turbo": 0.3,
        "gpt-4": 0.3,
        "dall-e": 0.3,
    }
    payment_link = config["STRIPE_PAYMENT_LINK"]
    stripe_public_key = config["STRIPE_API_PUBLISHABLE_KEY"]
    stripe_secret_key = config["STRIPE_API_SECRET_KEY"]
    stripe_webhook_secret = config["STRIPE_WEBHOOK_SECRET"]
    stripe_price_id = "price_1NAWLbHCGQv2kDWZu8N1uuOO"
    stripe_success_url = "https://s3m3dov.github.io/simple-success-page/"
    currency = "usd"
    phone_number_collection_enabled = True
    trial_period_days = 2

    @property
    def telegram_bot_token(self) -> str:
        """Telegram bot token."""
        return config["TELEGRAM_BOT_TOKEN"]

    @property
    def database_url(self) -> str:
        """Database url."""
        url = "{driver}://{user}:{password}@{host}:{port}/{database}".format(
            driver=config["DB_DRIVER"],
            user=config["DB_USER"],
            password=config["DB_PASSWORD"],
            host=config["DB_HOST"],
            port=config["DB_PORT"],
            database=config["DB_DATABASE"],
        )
        return url
