from typing import Optional
from pydantic import BaseModel


class ForumTopic(BaseModel):
    message_thread_id: int
    name: str
    icon_color: int
    icon_custom_emoji_id: Optional[str] = None