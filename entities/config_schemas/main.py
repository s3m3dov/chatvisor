from typing import Optional

from pydantic.main import BaseModel

from entities.enums import SystemUser


class TelegramConfig(BaseModel):
    """
    Config for Telegram
    """

    bot_token: str


class DBConfig(BaseModel):
    """
    Config for DB
    """

    driver: str
    user: str
    password: str
    host: str
    port: str
    database: str

    @property
    def uri(self) -> str:
        """Database url."""
        url = "{driver}://{user}:{password}@{host}:{port}/{database}"
        return url.format(
            driver=self.driver,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database,
        )


class LLMConfig(BaseModel):
    """
    Config for LLM
    """

    name: SystemUser
    temperature: float = 0.3
    max_tokens: int = 300
    free_tokens: int = 2000
    paid_tokens_per_day: int = 10000


class StripeConfig(BaseModel):
    """
    Config for Stripe
    """

    api_pub_key: str
    api_secret_key: str
    webhook_secret: str

    currency: str = "usd"

    success_url: str
    dashboard_url: str
    price_id: str
    trial_period_days: int
    phone_number_collection_enabled: bool = True

    payment_link: Optional[str]


