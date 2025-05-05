from typing import Optional
from pydantic import BaseModel, Field
from .maybe_inaccessible_message import MaybeInaccessibleMessage
from .user import User

class CallbackQuery(BaseModel):
    id: str
    user: User = Field(alias="from")
    message: Optional[MaybeInaccessibleMessage] = None
    inline_message_id: Optional[str] = None
    chat_instance: str
    data: Optional[str] = None
    game_short_name: Optional[str] = None