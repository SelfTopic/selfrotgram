from .base import BaseHandler 
from ..context import TContext
from ..types import HandlerType

class MessageHandler(BaseHandler[TContext]):
    ctx: TContext
    type: HandlerType = HandlerType.message

    def __init__(self, ctx: TContext) -> None:
        super().__init__(ctx)


   