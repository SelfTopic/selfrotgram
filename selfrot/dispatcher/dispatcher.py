from ..context import TContext
from ..router import BaseRouter 
from typing import (
    Generic, 
    List,
    AsyncGenerator,
    Type, 
    Any,
    Generator
)
from ..handlers import BaseHandler 
from ..middleware import BaseMiddleware
from ..client import Bot 
from ..types import Update

import asyncio

class BaseDispatcher(BaseRouter[TContext], Generic[TContext]): 

    bot: Type[Bot]
    handlers: List[Type[BaseHandler[TContext]]] = []
    middlewares: List[Type[BaseMiddleware[TContext]]] = []
    ctx: TContext

    def __init__(self) -> None:
        super().__init__()
        self.api = self.bot()

    
    def register_handler(
        self,
        handler: Type[BaseHandler[TContext]]
    ) -> None:
        self.handlers.append(handler)

    def register_middleware(
        self,
        middleware: Type[BaseMiddleware[TContext]]
    ) -> None:
        self.middlewares.append(middleware)

    
    async def call_middleware(self) -> bool:

        called_middlewares: List[BaseMiddleware[TContext]] = []

        for middleware in reversed(self.middlewares):
            called_middleware = middleware(self.ctx)
            pre = await asyncio.create_task(called_middleware.pre_handle())

            if pre == True:
                called_middlewares.append(called_middleware)
                continue 

            else: 
                return False
            
        
        await self.call_handler()

        for middleware in reversed(called_middlewares):
            await asyncio.create_task(middleware.post_handle())
            

        return True

    async def call_handler(self) -> None:

        for handler in self._get_type_handlers():
            result = await handler.filter()

            if result == True:
                await handler.pre_handle()
                await handler.handle()
            else:
                continue
            
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

    def _get_type_handlers(self) -> Generator[BaseHandler[TContext], Any, None]:
        for handler in self.handlers:
            called_handler = handler(self.ctx)
            if called_handler.check_type_ctx():
                yield called_handler
        

    async def polling(self) -> None:

        while True:
            async for update in self.poll_updates():
                self.ctx = self.context(update, self.api)

                await asyncio.create_task(self.call_middleware())

    async def _start(self, skip_updates):
        if skip_updates:
            await self.api.delete_webhook()
        await self.polling()

    def start_polling(self, skip_updates=True):
        asyncio.run(self._start(skip_updates))