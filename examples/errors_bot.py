import logging
import os

from selfrot import BaseContext, BaseDispatcher, Bot, MessageHandler
from selfrot.filter import Command
from selfrot.types import TextMessage


class UserError(Exception):
    """Ошибка, текст которой можно показать пользователю (остальные — баги)."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class NotEnoughMoney(UserError):
    def __init__(self, price: int, balance: int) -> None:
        super().__init__(f"Нужно {price}, а у тебя {balance}")
        self.price = price


def validate_name(name: str) -> str:
    if len(name) < 3:
        raise UserError("Имя короче 3 символов")

    return name


class Rename(MessageHandler[BaseContext[TextMessage]]):
    """/rename имя — проверка в pre_handle, ответ на UserError даёт диспетчер."""

    cmd = Command("rename", args_count=1)
    query = cmd

    async def pre_handle(self) -> None:
        self.name = validate_name(self.cmd.parse(self.ctx).args[0])

    async def handle(self) -> None:
        await self.ctx.answer_message(f"Теперь тебя зовут {self.name}")


class Buy(MessageHandler[BaseContext[TextMessage]]):
    """/buy — этот хендлер отвечает на NotEnoughMoney по-своему, остальное отдаёт выше."""

    query = Command("buy")

    async def handle(self) -> None:
        raise NotEnoughMoney(price=100, balance=30)

    async def on_error(self, exc: Exception) -> None:
        if isinstance(exc, NotEnoughMoney):
            await self.ctx.reply_message(f"Не хватает денег: {exc.message}")
            return

        raise exc


class Bug(MessageHandler[BaseContext[TextMessage]]):
    """/bug — обычный баг: пользователь не видит текста, в лог уходит трейсбек."""

    query = Command("bug")

    async def handle(self) -> None:
        raise ValueError("внутренняя ошибка")


class Dispatcher(BaseDispatcher[BaseContext]):
    bot = Bot
    context = BaseContext
    handlers = (Rename, Buy, Bug)

    async def on_error(self, ctx: BaseContext, exc: Exception) -> None:
        if isinstance(exc, UserError):
            await ctx.reply_message(exc.message)
            return

        await super().on_error(ctx, exc)  # лог; сюда можно добавить сообщение админу


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    Dispatcher(token=os.environ.get("BOT_TOKEN")).start_polling()
