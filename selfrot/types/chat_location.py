from pydantic import BaseModel
from .location import Location


class ChatLocation(BaseModel):
    location: Location
    address: str