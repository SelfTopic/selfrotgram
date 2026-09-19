from abc import abstractmethod, ABC
from typing import Generic, Any, Optional
from ..context import TContext

class BaseMiddleware(ABC, Generic[TContext]):
    ctx: TContext

    def __init__(self, ctx: TContext) -> None:
        super().__init__()
        self.ctx = ctx

    @abstractmethod
    async def pre_handle(self) -> bool: ...

    @abstractmethod
    async def post_handle(self, exc: Optional[BaseException] = None) -> Any:
        """
        exc — исключение, вылетевшее из handle() (или из другого middleware
        глубже по цепочке), либо None если всё прошло успешно. Передаётся
        явно диспетчером — не introspection через sys.exc_info().
        """
        ...
