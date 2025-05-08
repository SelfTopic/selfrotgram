from typing import Optional
from pydantic import BaseModel

class InputContactMessageContent(BaseModel):
    phone_number: str
    first_name: str
    last_name: Optional[str] = None
    vcard: Optional[str] = None