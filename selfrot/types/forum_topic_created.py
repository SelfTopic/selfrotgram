from typing import Optional
from pydantic import BaseModel

class ForumTopicCreated(BaseModel):
    name: str
    icon_color: int
    icon_custom_emoji_id: Optional[str] = None