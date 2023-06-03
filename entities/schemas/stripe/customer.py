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
    object: str
    address: Address
    balance: float
    created: int
    currency: Optional[str]
    default_currency: Optional[str]
    default_source: Optional[str]
    delinquent: bool
    description: Optional[str]
    discount: Optional[float]
    email: str
    id: str
    invoice_prefix: str
    invoice_settings: InvoiceSettings
    livemode: bool
    metadata: Optional[dict]
    name: str
    next_invoice_sequence: int
    phone: str
    preferred_locales: List[str]
    shipping: Any
    tax_exempt: str
    test_clock: Optional[str]
