from pydantic import BaseModel

class AcceptedGiftTypes(BaseModel):
    unlimited_gifts: bool
    limited_gifts: bool
    unique_gifts: bool
    premium_subscription: bool