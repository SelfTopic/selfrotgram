from typing import List, Optional
from pydantic import BaseModel
from .chat import Chat
from .reaction_type import ReactionType
from .user import User

class MessageReactionUpdated(BaseModel):
    chat: Chat
    message_id: int
    user: Optional[User] = None
    actor_chat: Optional[Chat] = None
    date: int
    old_reaction: List[ReactionType]
    new_reaction: List[ReactionType]