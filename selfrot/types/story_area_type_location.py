from typing import Optional
from pydantic import BaseModel
from .location_address import LocationAddress

class StoryAreaTypeLocation(BaseModel):
    type: str
    latitude: float
    longitude: float
    address: Optional[LocationAddress] = None