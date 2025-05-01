from abc import abstractmethod, ABC 
from typing import Generic, Any
from ..context import TContext

class BaseMiddleware(ABC, Generic[TContext]):
    ctx: TContext
    
    def __init__(self, ctx: TContext) -> None:
        super().__init__()
        self.ctx = ctx
    
    @abstractmethod
    async def pre_handle(self) -> bool: ...

    @abstractmethod
    async def post_handle(self) -> Any: ...
