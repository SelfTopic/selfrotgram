import logging
import os

from selfrot import BaseContext, BaseDispatcher, Bot
from selfrot.filter import MemberJoined, MemberLeft
from selfrot.handlers import ChatMemberHandler, MyChatMemberHandler
from selfrot.types import ChatMemberUpdated

# Порт chat_member_update_routers из chestor_bot (без БД): вход и выход участников.
# JOIN_TRANSITION и LEAVE_TRANSITION из aiogram — это MemberJoined и MemberLeft.

WELCOME = "Добро пожаловать!"
GOODBYE = "Пока!"


class BotAdded(MyChatMemberHandler[BaseContext[ChatMemberUpdated]]):
    """my_chat_member: изменился статус самого бота."""

    query = MemberJoined()

    async def handle(self) -> None:
        await self.ctx.my_chat_member.answer("Меня добавили в чат")


class NewMember(ChatMemberHandler[BaseContext[ChatMemberUpdated]]):
    """chat_member: изменился статус другого участника (бот должен быть админом)."""

    query = MemberJoined()

    async def handle(self) -> None:
        event = self.ctx.chat_member
        if not event.new_chat_member.user.is_bot:
            await event.answer(WELCOME)


class MemberGone(ChatMemberHandler[BaseContext[ChatMemberUpdated]]):
    query = MemberLeft()  # вышел, удалён или заблокирован

    async def handle(self) -> None:
        await self.ctx.chat_member.answer(GOODBYE)


class Dispatcher(BaseDispatcher[BaseContext]):
    bot = Bot
    context = BaseContext
    handlers = (BotAdded, NewMember, MemberGone)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    # allowed_updates соберётся сам: chat_member и my_chat_member Telegram по
    # умолчанию не присылает, а библиотека просит их ровно потому, что есть хендлеры.
    Dispatcher(token=os.environ.get("BOT_TOKEN")).start_polling()
