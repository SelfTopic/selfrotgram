from typing import Optional
from pydantic import BaseModel


class SwitchInlineQueryChosenChat(BaseModel):
    query: Optional[str] = None
    allow_user_chats: Optional[bool] = None
    allow_bot_chats: Optional[bool] = None
    allow_group_chats: Optional[bool] = None
    allow_channel_chats: Optional[bool] = None