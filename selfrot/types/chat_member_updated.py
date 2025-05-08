from typing import Optional
from pydantic import BaseModel, Field
from .chat import Chat
from .chat_invite_link import ChatInviteLink
from .user import User
from .chat_member import ChatMember

class ChatMemberUpdated(BaseModel):
    chat: Chat
    user: User = Field(alias="from")
    date: int
    old_chat_member: ChatMember
    new_chat_member: ChatMember
    invite_link: Optional[ChatInviteLink] = None
    via_join_request: Optional[bool] = None
    via_chat_folder_invite_link: Optional[bool] = None