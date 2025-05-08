from typing import Optional
from pydantic import BaseModel, Field
from ..types import Location
from ..types import User

class InlineQuery(BaseModel):
    id: str
    user: User = Field(alias="from")
    query: str
    offset: str
    chat_type: Optional[str] = None
    location: Optional[Location] = None