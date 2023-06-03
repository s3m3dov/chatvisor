from typing import List, Optional, Any

from pydantic.main import BaseModel

from .base import AutomaticTax


class CustomText(BaseModel):
    shipping_address: Optional[str]
    submit: Optional[str]


class CustomerDetails(BaseModel):
    address: Optional[str]
    email: Optional[str]
    name: Optional[str]
    phone: Optional[str]
    tax_exempt: str
    tax_ids: Optional[List[str]]


class PhoneNumberCollection(BaseModel):
    enabled: bool


class CheckoutSession(BaseModel):
    id: str
    object: str
    created: int

    mode: str
    status: str
    url: str
    success_url: str
    cancel_url: Optional[str]

    livemode: bool
    metadata: Optional[dict]

    after_expiration: Optional[str]
    allow_promotion_codes: Optional[str]
    amount_subtotal: Optional[str]
    amount_total: Optional[str]
    automatic_tax: AutomaticTax
    billing_address_collection: Optional[str]
    client_reference_id: Optional[str]
    consent: Optional[str]
    consent_collection: Optional[str]
    currency: Optional[str]
    currency_conversion: Optional[str]
    custom_fields: List[str]
    custom_text: CustomText
    customer: Optional[str]
    customer_creation: Optional[str]
    customer_details: Optional[CustomerDetails]
    customer_email: Optional[str]
    expires_at: int
    invoice: Optional[str]
    invoice_creation: Optional[str]
    locale: Optional[str]
    payment_intent: Optional[str]
    payment_link: Optional[str]
    payment_method_collection: Optional[str]
    payment_method_options: Optional[dict]
    payment_method_types: List[str]
    payment_status: str
    phone_number_collection: PhoneNumberCollection
    recovered_from: Optional[str]
    setup_intent: Optional[str]
    shipping_address_collection: Optional[str]
    shipping_cost: Optional[str]
    shipping_details: Optional[str]
    shipping_options: List[str]
    submit_type: Optional[str]
    subscription: Optional[str]
    total_details: Optional[Any]
