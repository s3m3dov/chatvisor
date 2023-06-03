from typing import List, Optional

from pydantic import BaseModel

from .base import Plan, Price, Period, AutomaticTax, Address, PaymentSettings


class ProrationDetails(BaseModel):
    credited_items: Optional[List[dict]]


class LineItem(BaseModel):
    id: str
    object: str
    amount: int
    amount_excluding_tax: int
    currency: str
    description: str
    discount_amounts: List[dict]
    discountable: bool
    discounts: List[dict]
    livemode: bool
    metadata: dict
    period: Period
    plan: Plan
    price: Price
    proration: bool
    proration_details: ProrationDetails
    quantity: int
    subscription: str
    subscription_item: str
    tax_amounts: List[dict]
    tax_rates: List[dict]
    type: str
    unit_amount_excluding_tax: str


class Lines(BaseModel):
    object: str
    data: List[LineItem]
    has_more: bool
    total_count: int
    url: str


class StatusTransitions(BaseModel):
    finalized_at: int
    marked_uncollectible_at: Optional[int]
    paid_at: int
    voided_at: Optional[int]


class Invoice(BaseModel):
    id: str
    object: str
    account_country: str
    account_name: str
    account_tax_ids: Optional[None]
    amount_due: int
    amount_paid: int
    amount_remaining: int
    amount_shipping: int
    application: Optional[str]
    application_fee_amount: Optional[str]
    attempt_count: int
    attempted: bool
    auto_advance: bool
    automatic_tax: AutomaticTax
    billing_reason: str
    charge: Optional[str]
    collection_method: str
    created: int
    currency: str
    custom_fields: Optional[None]
    customer: str
    customer_address: Address
    customer_email: str
    customer_name: str
    customer_phone: str
    customer_shipping: Optional[str]
    customer_tax_exempt: str
    customer_tax_ids: List[str]
    default_payment_method: Optional[str]
    default_source: Optional[str]
    default_tax_rates: List[str]
    description: Optional[str]
    discount: Optional[str]
    discounts: List[dict]
    due_date: Optional[str]
    ending_balance: int
    footer: Optional[str]
    from_invoice: Optional[str]
    hosted_invoice_url: str
    invoice_pdf: str
    last_finalization_error: Optional[str]
    latest_revision: Optional[str]
    lines: Lines
    livemode: bool
    metadata: dict
    next_payment_attempt: Optional[str]
    number: str
    on_behalf_of: Optional[str]
    paid: bool
    paid_out_of_band: bool
    payment_intent: Optional[str]
    payment_settings: PaymentSettings
    period_end: int
    period_start: int
    post_payment_credit_notes_amount: int
    pre_payment_credit_notes_amount: int
    quote: Optional[str]
    receipt_number: Optional[str]
    rendering_options: Optional[str]
    shipping_cost: Optional[str]
    shipping_details: Optional[str]
    starting_balance: int
    statement_descriptor: Optional[str]
    status: str
    status_transitions: StatusTransitions
    subscription: str
    subtotal: int
    subtotal_excluding_tax: int
    tax: Optional[str]
    test_clock: Optional[str]
    total: int
    total_discount_amounts: List[dict]
    total_excluding_tax: int
    total_tax_amounts: List[dict]
    transfer_data: Optional[str]
    webhooks_delivered_at: Optional[str]
