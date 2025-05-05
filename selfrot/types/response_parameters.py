from typing import Optional
from pydantic import BaseModel


class ResponseParameters(BaseModel):
    migrate_to_chat_id: Optional[int] = None
    retry_after: Optional[int] = None