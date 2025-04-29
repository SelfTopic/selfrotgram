from ..context import BaseContext 

from abc import abstractmethod

class BaseMiddleware:
    context: type[BaseContext]
    
    @abstractmethod
    async def pre_handle(self, ctx: type[BaseContext]): ...

    @abstractmethod
    async def post_handle(self, ctx: type[BaseContext]): ...
