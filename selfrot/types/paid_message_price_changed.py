from pydantic import BaseModel

class PaidMessagePriceChanged(BaseModel):
    paid_message_star_count: int