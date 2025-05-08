from pydantic import BaseModel

class LabeledPrice(BaseModel):
    label: str
    amount: int