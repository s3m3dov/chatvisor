from typing import Optional

from pydantic.main import BaseModel


class Address(BaseModel):
    """Address model."""

    city: str
    country: str
    line1: Optional[str]
    line2: Optional[str]
    postal_code: Optional[str]
    state: Optional[str]


class AutomaticTax(BaseModel):
    enabled: bool
    status: Optional[str]


class Period(BaseModel):
    end: int
    start: int


class Recurring(BaseModel):
    aggregate_usage: Optional[str]
    interval: str
    interval_count: int
    trial_period_days: Optional[int]
    usage_type: str


class Price(BaseModel):
    id: str
    object: str
    active: bool
    billing_scheme: str
    created: int
    currency: str
    custom_unit_amount: Optional[int]
    livemode: bool
    lookup_key: Optional[str]
    metadata: Optional[dict]
    nickname: Optional[str]
    product: str
    recurring: Recurring
    tax_behavior: str
    tiers_mode: Optional[str]
    transform_quantity: Optional[str]
    type: str
    unit_amount: int
    unit_amount_decimal: str


class Plan(BaseModel):
    id: str
    object: str
    active: bool
    aggregate_usage: Optional[str]
    amount: int
    amount_decimal: str
    billing_scheme: str
    created: int
    currency: str
    interval: str
    interval_count: int
    livemode: bool
    metadata: Optional[dict]
    nickname: Optional[str]
    product: str
    tiers_mode: Optional[str]
    transform_usage: Optional[str]
    trial_period_days: Optional[int]
    usage_type: str


class PaymentSettings(BaseModel):
    default_mandate: Optional[str]
    payment_method_options: Optional[str]
    payment_method_types: Optional[str]
