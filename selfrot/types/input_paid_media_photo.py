from pydantic import BaseModel

class InputPaidMediaPhoto(BaseModel):
    type: str
    media: str