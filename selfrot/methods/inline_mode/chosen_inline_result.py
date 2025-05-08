from typing import Optional
from pydantic import BaseModel, Field
from ..types import Location
from ..types import User

class ChosenInlineResult(BaseModel):
    result_id: str
    user: User = Field(alias="from")
    location: Optional[Location] = None
    inline_message_id: Optional[str] = None
    query: str