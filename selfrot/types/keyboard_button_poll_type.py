from typing import Optional
from pydantic import BaseModel

class KeyboardButtonPollType(BaseModel):
    type: Optional[str] = None