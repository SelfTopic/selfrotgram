from typing import Optional
from pydantic import BaseModel

class ForceReply(BaseModel):
    force_reply: bool
    input_field_placeholder: Optional[str] = None
    selective: Optional[bool] = None