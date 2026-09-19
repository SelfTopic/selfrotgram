import logging
import os

from selfrot import BaseContext, BaseDispatcher, Bot, MessageHandler
from selfrot.filter import HasText
from selfrot.middleware import LoggingMiddleware
from selfrot.types import TextMessage


class EchoHandler(MessageHandler[BaseContext[TextMessage]]):
    query = HasText()

    async def handle(self) -> None:
        # message.text — str: HasText уже проверил, что текст есть.
        await self.ctx.answer_message(f"Echo: {self.ctx.message.text}")


class Dispatcher(BaseDispatcher[BaseContext[TextMessage]]):
    bot = Bot
    context = BaseContext
    handlers = (EchoHandler,)
    middlewares = (LoggingMiddleware,)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s"
    )
    logging.basicConfig(level=logging.INFO)

    dp = Dispatcher(token=os.environ.get("BOT_TOKEN"))
    dp.start_polling()
