from typing import Optional
from pydantic import BaseModel

class SentWebAppMessage(BaseModel):
    inline_message_id: Optional[str] = None