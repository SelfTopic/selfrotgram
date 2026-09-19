import logging
import os
from dataclasses import dataclass

from selfrot import BaseContext, BaseDispatcher, Bot, MessageHandler
from selfrot.types import Update


class GreetingService:
    """Простая зависимость — не имеет отношения к Telegram API."""

    def greet(self, name: str) -> str:
        return f"Здарова, {name}!"


@dataclass
class DepsContext(BaseContext):
    greeter: GreetingService


class GreetHandler(MessageHandler):
    ctx: DepsContext

    async def handle(self):
        user = self.ctx.user
        name = user.first_name if user else "незнакомец"

        await self.ctx.answer_message(self.ctx.greeter.greet(name))


class Dispatcher(BaseDispatcher):
    bot = Bot
    context = DepsContext
    handlers = (GreetHandler,)
    middlewares = ()

    def __init__(self, token: str | None = None) -> None:
        super().__init__(token)
        self.greeter = GreetingService()

    def create_context(self, update: Update) -> DepsContext:
        return self.context(update, self.api, self.greeter)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    dp = Dispatcher(token=os.environ.get("BOT_TOKEN"))
    dp.start_polling()
