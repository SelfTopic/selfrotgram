from typing import Optional
from pydantic import BaseModel


class LocationAddress(BaseModel):
    country_code: str
    state: Optional[str] = None
    city: Optional[str] = None
    street: Optional[str] = None