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
        handler: Type[BaseHandler[TContext]]
    ) -> None:
        self.handlers.append(handler(self.ctx))

    

    async def call_handler(self) -> None:

        async for handler in self._get_type_handlers():
            result = await handler.filter()

            if result == True:
                await handler.pre_handle()
                await handler.handle()

            else:
                return None
            
    async def poll_updates(self) -> AsyncGenerator[Update, None]:

        offset = 0 
        while True:

            try:

                updates = await self.api.get_updates(offset=offset)
                
                if updates:
                    offset = updates[-1].update_id + 1 

                for update in updates:
                    yield update

            except Exception as e:
                print("Error get updates: ", e)

    async def _get_type_handlers(self) -> AsyncGenerator[BaseHandler[TContext], None]:
        for handler in self.handlers:
            if handler.check_type_ctx():
                yield handler
        

    async def polling(self) -> None:

        while True:
            async for update in self.poll_updates():
                self.ctx = self.context(update, self.api)

                await asyncio.create_task(self.call_handler())

    def start_polling(self):
        asyncio.run(self.polling())