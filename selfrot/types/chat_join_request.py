from typing import Optional
from pydantic import BaseModel, Field
from .chat import Chat
from .chat_invite_link import ChatInviteLink
from .user import User

class ChatJoinRequest(BaseModel):
    chat: Chat
    user: User = Field(alias="from")
    user_chat_id: int
    date: int
    bio: Optional[str] = None
    invite_link: Optional[ChatInviteLink] = None