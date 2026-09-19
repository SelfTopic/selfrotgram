from selfrot import MessageHandler
from selfrot.filter import Text
from selfrot.types import TextMessage

from .context import AppContext


class BotHandler(MessageHandler[AppContext[TextMessage]]):
    query = Text("бот", ignore_case=True)

    async def handle(self) -> None:
        await self.ctx.answer_message(self.ctx.dialogs.random("bot"))
