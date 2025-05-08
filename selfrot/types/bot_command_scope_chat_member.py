from typing import Union
from pydantic import BaseModel

class BotCommandScopeChatMember(BaseModel):
    type: str
    chat_id: Union[int, str]
    user_id: int