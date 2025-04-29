from abc import ABC
from ..context.context import TContext
from typing import Generic, Type

class BaseRouter(ABC, Generic[TContext]):
    context: Type[TContext]
    ctx: TContext

    def __init__(self) -> None:
        super().__init__()

