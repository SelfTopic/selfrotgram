from typing import Optional
from pydantic import BaseModel

class ForumTopicEdited(BaseModel):
    name: Optional[str] = None
    icon_custom_emoji_id: Optional[str] = None