import logging
import os
from typing import Any

from selfrot import BaseContext, BaseDispatcher, Bot, MessageHandler
from selfrot.filter import BaseFilter, HasText
from selfrot.types import TextMessage

# Свой фильтр: достаточно написать check(). Ничего объявлять не нужно.


class IsPrivate(BaseFilter[BaseContext[Any]]):
    """Сообщение из личного чата, а не из группы."""

    async def check(self, ctx: BaseContext[Any]) -> bool:
        chat = ctx.chat
        return chat is not None and chat.type == "private"


class PrivateEcho(MessageHandler[BaseContext[TextMessage]]):
    # & — оба фильтра сразу. HasText гарантирует текст, поэтому text здесь str.
    query = HasText() & IsPrivate()

    async def handle(self) -> None:
        await self.ctx.message.answer(f"Только между нами: {self.ctx.message.text}")


class GroupNote(MessageHandler[BaseContext[TextMessage]]):
    # ~ — «не»: любой текст, кроме личного чата.
    query = HasText() & ~IsPrivate()

    async def handle(self) -> None:
        await self.ctx.message.answer("В группах я не эхо-бот, напиши мне в личку.")


class Dispatcher(BaseDispatcher[BaseContext]):
    bot = Bot
    context = BaseContext
    handlers = (PrivateEcho, GroupNote)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s"
    )
    Dispatcher(token=os.environ.get("BOT_TOKEN")).start_polling()
