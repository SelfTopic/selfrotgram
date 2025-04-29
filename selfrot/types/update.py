from pydantic import BaseModel
from .message import Message 
from typing import Optional

class Update(BaseModel):
    message: Optional[Message]
    update_id: int 