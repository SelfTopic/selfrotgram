import logging
import os

from selfrot import (
    BaseContext,
    BaseDispatcher,
    BaseMiddleware,
    BaseTask,
    Bot,
    Every,
    MessageHandler,
)
from selfrot.filter import Command
from selfrot.types import TextMessage

# Фоновая периодическая задача: Dispatcher.tasks. Задача получает тот же вид ctx, что
# и хендлер, прошедший те же мидлвари диспетчера — разница только в ctx.is_background
# (апдейта за задачей нет вовсе, ctx.chat/ctx.user и подобное — None).

ACTIVE_CHATS: set[int] = set()


class TrackActivity(BaseMiddleware[BaseContext]):
    """Настоящая мидлварь (сессия БД, сервисы) видит is_background и сама решает,
    что делать с фоновым тиком — здесь просто не трогаем ACTIVE_CHATS, если апдейта
    не было вовсе."""

    async def pre_handle(self) -> bool:
        return True

    async def post_handle(self, exc: BaseException | None = None) -> None:
        if not self.ctx.is_background and self.ctx.chat is not None:
            ACTIVE_CHATS.add(self.ctx.chat.id)


class Hello(MessageHandler[BaseContext[TextMessage]]):
    query = Command("hello")

    async def handle(self) -> None:
        await self.ctx.message.reply("Привет! Запомнил этот чат.")


class ReportActiveChats(BaseTask[BaseContext]):
    """Every(5, ReportActiveChats) — раз в 5 секунд печатает, сколько чатов писало
    боту. TrackActivity отработала и для этого вызова (pre_handle/post_handle), просто
    is_background=True сказал ей ничего не добавлять в ACTIVE_CHATS."""

    async def run(self) -> None:
        logging.info("Активных чатов: %s", len(ACTIVE_CHATS))


class Dispatcher(BaseDispatcher[BaseContext]):
    bot = Bot
    context = BaseContext
    middlewares = (TrackActivity,)
    handlers = (Hello,)
    tasks = (Every(5, ReportActiveChats),)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    Dispatcher(token=os.environ.get("BOT_TOKEN")).start_polling()
