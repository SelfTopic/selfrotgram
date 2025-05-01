from abc import ABC, abstractmethod
from ..context import TContext
from ..types import HandlerType
from typing import Generic, Any

class BaseHandler(ABC, Generic[TContext]):
    ctx: TContext
    type: HandlerType 
    def __init__(self, ctx: TContext) -> None:
        self.ctx = ctx

    @abstractmethod
    async def handle(self) -> Any: ...

    async def pre_handle(self) -> Any: ...

    async def filter(self) -> bool: 
        return True
    
    def check_type_ctx(self): 
        if self.ctx.message and self.type.value == "message":
            return True 
        
        else:
            return False