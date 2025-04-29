from ..context import TContext
from ..router import BaseRouter 
from typing import (
    Generic, 
    List,
    AsyncGenerator,
    Type
)
from ..handlers import BaseHandler
from ..client import Bot 
from ..types import Update

import asyncio

class BaseDispatcher(BaseRouter[TContext], Generic[TContext]): 

    bot: Type[Bot]
    handlers: List[BaseHandler[TContext]] = []

    def __init__(self) -> None:
        super().__init__()
        self.api = self.bot()
    
    def register_handler(
        self,
        handler: BaseHandler[TContext]
    ) -> None:
        self.handlers.append(handler)

    

    async def call_handler(self) -> None:

        for handler in self.handlers:
            result = await handler.filter(self.ctx)

            if result == True:
                await handler.pre_handle(self.ctx)
                await handler.handle(self.ctx)

            else:
                return None
            
    async def poll_updates(self) -> AsyncGenerator[Update, None]:

        offset = 0 
        while True:

            try:

                response = await self.api.get_updates(offset=offset)
                
                updates = [Update(**u) for u in response.get("result", [])]
                if updates:
                    offset = updates[-1].update_id + 1 

                for update in updates:
                    yield update

            except Exception as e:
                print("Error get updates: ", e)

    async def polling(self) -> None:

        while True:
            async for update in self.poll_updates():
                self.ctx = self.context(update, self.api)

                await asyncio.create_task(self.call_handler())

    def start(self):
        asyncio.run(self.polling())