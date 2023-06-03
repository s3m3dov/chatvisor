from typing import List, Optional

from pydantic.main import BaseModel

from .base import Plan, Price, AutomaticTax, PaymentSettings


class SubscriptionItem(BaseModel):
    id: str
    object: str
    billing_thresholds: Optional[List[int]]
    created: int
    metadata: Optional[dict]
    plan: Plan
    price: Price
    quantity: int
    subscription: str
    tax_rates: Optional[List[str]]


class SubscriptionItems(BaseModel):
    object: str
    data: List[SubscriptionItem]
    has_more: bool
    total_count: int
    url: str


class EndBehavior(BaseModel):
    missing_payment_method: str


class TrialSettings(BaseModel):
    end_behavior: EndBehavior


class CancellationDetails(BaseModel):
    reason: Optional[str]
    feedback: Optional[str]
    comment: Optional[str]


class CustomerSubscription(BaseModel):
    id: str
    object: str
    status: str
    customer: str

    created: int

    cancel_at: Optional[int]
    canceled_at: Optional[int]
    cancel_at_period_end: bool
    cancellation_details: CancellationDetails

    current_period_end: int
    current_period_start: int

    days_until_due: Optional[int]
    start_date: int
    ended_at: Optional[int]

    trial_end: Optional[int]
    trial_start: Optional[int]
    trial_settings: TrialSettings

    metadata: Optional[dict]
    livemode: bool

    items: SubscriptionItems
    plan: Plan
    quantity: int

    currency: str
    latest_invoice: str

    application: Optional[str]
    application_fee_percent: Optional[int]
    automatic_tax: AutomaticTax
    billing_cycle_anchor: int
    billing_thresholds: Optional[List[int]]
    collection_method: str
    default_payment_method: str
    default_source: Optional[str]
    default_tax_rates: Optional[List[str]]
    description: Optional[str]
    discount: Optional[str]
    next_pending_invoice_item_invoice: Optional[str]
    on_behalf_of: Optional[str]
    pause_collection: Optional[bool]
    payment_settings: PaymentSettings
    pending_invoice_item_interval: Optional[int]
    pending_setup_intent: Optional[str]
    pending_update: Optional[dict]
    schedule: Optional[str]
    test_clock: Optional[str]
    transfer_data: Optional[dict]
