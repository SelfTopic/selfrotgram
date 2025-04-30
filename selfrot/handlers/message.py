from .base import BaseHandler 
from ..context import TContext
from ..types import HandlerType

class MessageHandler(BaseHandler[TContext]):
    ctx: TContext
    type: HandlerType = HandlerType.message

    def __init__(self, ctx: TContext) -> None:
        message = ctx.update_message_type_for_message_handler()
        ctx.message = message
        super().__init__(ctx)


   