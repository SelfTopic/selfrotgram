from typing import Union
from pydantic import BaseModel


class BotCommandScopeChat(BaseModel):
    type: str
    chat_id: Union[int, str]