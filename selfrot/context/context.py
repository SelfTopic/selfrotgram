from typing import TypeVar, Optional
from ..types import (
    Update,
    Message
)
from ..client import Bot
from dataclasses import dataclass


TContext = TypeVar("TContext", bound="BaseContext")  

@dataclass
class BaseContext:
    
    update: Update 
    bot: Bot

    @property 
    def message(self) -> Optional[Message]:
        return self.update.message
    
    async def reply(self, text: str):
        if not self.message:
            raise
        return await self.bot.send_message(text=text, chat_id=self.message.chat.id)



