from typing import List, Optional
from pydantic import BaseModel
from .chat import Chat
from .user import User

class PollAnswer(BaseModel):
    poll_id: str
    voter_chat: Optional[Chat] = None
    user: Optional[User] = None
    option_ids: List[int]