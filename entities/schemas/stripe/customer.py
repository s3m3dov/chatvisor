from typing import List, Any, Optional

from pydantic.main import BaseModel

from .base import Address


class InvoiceSettings(BaseModel):
    """Invoice settings model."""
    custom_fields: Optional[List[str]]
    default_payment_method: Optional[str]
    footer: Optional[str]
    rendering_options: Optional[str]


class Customer(BaseModel):
    """Customer model."""
    id: str
    object: str
    created: int

    metadata: Optional[dict]
    livemode: Optional[bool]

    name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    address: Optional[Address]
    balance: Optional[float]

    currency: Optional[str]
    default_currency: Optional[str]
    default_source: Optional[str]
    delinquent: Optional[bool]
    description: Optional[str]
    discount: Optional[float]
    invoice_prefix: Optional[str]
    invoice_settings: Optional[InvoiceSettings]
    next_invoice_sequence: Optional[int]
    preferred_locales: List[str]
    shipping: Optional[Any]
    tax_exempt: Optional[str]
    test_clock: Optional[str]
