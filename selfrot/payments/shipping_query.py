from pydantic import BaseModel, Field
from .shipping_address import ShippingAddress
from ..types import User

class ShippingQuery(BaseModel):
    id: str
    user: User = Field(alias="from")
    invoice_payload: str
    shipping_address: ShippingAddress