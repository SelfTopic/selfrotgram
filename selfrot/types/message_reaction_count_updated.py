from typing import List
from pydantic import BaseModel
from .chat import Chat
from .reaction_count import ReactionCount

class MessageReactionCountUpdated(BaseModel):
    chat: Chat
    message_id: int
    date: int
    reactions: List[ReactionCount]