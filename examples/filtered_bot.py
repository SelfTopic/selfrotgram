import logging
import os
from typing import cast

from selfrot import BaseContext, BaseDispatcher, Bot, MessageHandler
from selfrot.filter import BaseFilter
from selfrot.types import Message


class MessageContext(BaseContext):
    @property
    def message(self) -> Message:
        # .message уже существует на BaseContext как Optional[Message] —
        # мы не придумываем новое поле, только снимаем Optional с существующего.
        return cast(Message, super().message)


class HasMessage(BaseFilter[MessageContext]):
    async def check(self, ctx: BaseContext) -> bool:
        return ctx.message is not None


class TextHandler(MessageHandler[MessageContext]):
    query = HasMessage()

    async def handle(self) -> None:
        # ctx.message: Message, не Optional[Message] — без if/assert.
        await self.ctx.answer_message(f"Echo: {self.ctx.message.text or ''}")


class Dispatcher(BaseDispatcher[BaseContext]):
    bot = Bot
    context = BaseContext
    handlers = (TextHandler,)
    middlewares = ()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    dp = Dispatcher(token=os.environ.get("BOT_TOKEN"))
    dp.start_polling()
