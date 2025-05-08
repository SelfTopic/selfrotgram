from typing import Optional
from pydantic import BaseModel
from ..types import Chat
from ..types import Gift

class TransactionPartnerChat(BaseModel):
    type: str
    chat: Chat
    gift: Optional[Gift] = None