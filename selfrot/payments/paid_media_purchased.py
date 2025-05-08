from pydantic import BaseModel, Field
from ..types import User

class PaidMediaPurchased(BaseModel):
    user: User = Field(alias="from")
    paid_media_payload: str