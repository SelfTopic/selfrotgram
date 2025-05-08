from typing import List
from pydantic import BaseModel
from .user import User

class VideoChatParticipantsInvited(BaseModel):
    users: List[User]