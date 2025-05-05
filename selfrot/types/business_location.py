from typing import Optional
from pydantic import BaseModel
from .location import Location

class BusinessLocation(BaseModel):
    address: str
    location: Optional[Location] = None