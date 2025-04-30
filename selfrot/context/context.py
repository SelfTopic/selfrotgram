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

    def __init_subclass__(cls) -> None:
        cls.message: Optional[Message] = cls.update.message
            
    async def reply(self, text: str):
        if not self.message:
            raise
        return await self.bot.send_message(text=text, chat_id=self.message.chat.id)
    
    def update_message_type_for_message_handler(self):
        if not self.message:
            raise 

        return self.message



