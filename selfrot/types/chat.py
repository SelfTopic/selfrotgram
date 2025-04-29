from pydantic import BaseModel 
from typing import Optional 

class Chat(BaseModel):

    id: int 
    title: Optional[str] = None
    username: Optional[str]
    first_name: str
    type: str
