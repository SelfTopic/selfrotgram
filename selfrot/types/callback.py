from pydantic import BaseModel, Field 
from typing import Optional
from .user import User

class CallbackQuery(BaseModel):

    user: Optional[User] = Field(alias='from')
    data: str 
