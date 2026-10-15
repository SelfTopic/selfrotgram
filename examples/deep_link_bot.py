import logging
import os

from selfrot import BaseContext, BaseDispatcher, Bot, MessageHandler, StartPayload
from selfrot.filter import Command
from selfrot.types import TextMessage

# Deep link: t.me/<bot>?start=... — Telegram сам превращает переход по ссылке в
# обычное сообщение "/start <то, что после start=>". Параметр ограничен Telegram
# алфавитом [A-Za-z0-9_-] и 64 символами (иначе ссылка молча портится), поэтому
# StartPayload — не то же самое, что CallbackPayload (у кнопок алфавит шире).


class MarryLink(StartPayload, prefix="marry"):
    proposer_id: int


marry = Command("start", MarryLink, deep_link=True)
start = Command("start", deep_link=True)


class Propose(MessageHandler[BaseContext[TextMessage]]):
    query = Command("propose")

    async def handle(self) -> None:
        user = self.ctx.message.user
        if user is None:
            return

        link = MarryLink(proposer_id=user.id).url(self.ctx.bot)
        await self.ctx.message.reply(f"Отправь эту ссылку второй половине:\n{link}")


class AcceptMarriage(MessageHandler[BaseContext[TextMessage]]):
    # query достаёт только свой deep link — Command("start", deep_link=True) ниже
    # не перехватит его первым, даже стоя выше в handlers (порядок не важен).
    query = marry

    async def handle(self) -> None:
        args = marry.parse(self.ctx)
        accepter = self.ctx.message.user
        if accepter is None:
            return

        await self.ctx.message.reply(
            f"Поздравляем! Брак заключён между {args.proposer_id} и {accepter.id}."
        )


class Start(MessageHandler[BaseContext[TextMessage]]):
    # Намеренно стоит ВЫШЕ AcceptMarriage в handlers — deep_link=True сам не
    # заберёт чужую ссылку, костыль с порядком не нужен.
    query = start

    async def handle(self) -> None:
        await self.ctx.message.reply(
            "Привет! Позови кого-нибудь в законный брак: /propose"
        )


class Dispatcher(BaseDispatcher[BaseContext]):
    bot = Bot
    context = BaseContext
    handlers = (Start, Propose, AcceptMarriage)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    Dispatcher(token=os.environ.get("BOT_TOKEN")).start_polling()
