from abc import ABC, abstractmethod
from ..context import TContext
from typing import Generic, Any

class BaseHandler(ABC, Generic[TContext]):
    
    def __init__(self) -> None:
        pass 

    @abstractmethod
    async def handle(self, ctx: TContext) -> Any: ...

    async def pre_handle(self, ctx: TContext) -> Any: ...

    async def filter(self, ctx: TContext) -> bool: 
        return True
    
    async def check_type_ctx(self): pass