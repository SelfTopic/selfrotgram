from typing import Union
from pydantic import BaseModel


class BotCommandScopeChatAdministrators(BaseModel):
    type: str
    chat_id: Union[int, str]