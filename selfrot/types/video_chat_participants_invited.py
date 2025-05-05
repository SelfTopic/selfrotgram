from typing import List
from pydantic import BaseModel


class VideoChatParticipantsInvited(BaseModel):
    users: List[User]