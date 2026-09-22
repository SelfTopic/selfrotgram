import logging
import os
from typing import Literal

from selfrot import BaseContext, BaseDispatcher, Bot, CommandArgs, MessageHandler, Rest
from selfrot.exceptions import CommandArgsError
from selfrot.filter import AnyCommand, Command
from selfrot.types import TextMessage

# Аргументы команды как данные: описали форму один раз, а библиотека разобрала, проверила
# и привела типы. Хендлер получает готовый объект.


class CalcArgs(CommandArgs):
    one: int
    operator: Literal["+", "-", "*", "/"]  # только эти четыре; тип виден редактору
    two: int


class SayArgs(CommandArgs):
    times: int = 1  # значение по умолчанию: аргумент можно не писать (только с конца)
    text: Rest = ""  # Rest забирает весь остаток строки, с пробелами


class TransferArgs(CommandArgs):
    to: str
    amount: int


class Calc(MessageHandler[BaseContext[TextMessage]]):
    cmd = Command("calc", CalcArgs)
    query = cmd

    async def pre_handle(self) -> None:
        # Неверные аргументы бросают CommandArgsError: до handle дело не дойдёт.
        self.args = self.cmd.parse(self.ctx)

    async def handle(self) -> None:
        a = self.args  # CalcArgs: one и two это int, operator это Literal
        match a.operator:
            case "+":
                result = a.one + a.two
            case "-":
                result = a.one - a.two
            case "*":
                result = a.one * a.two
            case "/":
                result = a.one / a.two if a.two else "на ноль делить нельзя"

        await self.ctx.message.answer(f"{a.one} {a.operator} {a.two} = {result}")


class Say(MessageHandler[BaseContext[TextMessage]]):
    cmd = Command("say", SayArgs)
    query = cmd

    async def handle(self) -> None:
        args = self.cmd.parse(self.ctx)
        text = args.text or "Что сказать?"
        await self.ctx.message.answer("\n".join([text] * min(args.times, 5)))


# Одна команда, несколько слов-вызовов: у каждого своё имя, префиксы и регистр, а форма
# аргументов общая. Подходит любое; parse разбирает аргументы того слова, что сработало.
TRANSFER = AnyCommand(
    Command("transfer", TransferArgs, ignore_case=True),
    Command("перевести", TransferArgs, prefixes="", ignore_case=True),
    Command("кинуть", TransferArgs, prefixes="", ignore_case=True),
)


class Transfer(MessageHandler[BaseContext[TextMessage]]):
    query = TRANSFER

    async def handle(self) -> None:
        args = TRANSFER.parse(self.ctx)  # TransferArgs, каким бы словом ни позвали
        word = TRANSFER.find(self.ctx).name  # а какое слово это было
        await self.ctx.message.answer(f"Переведено {args.amount} для {args.to} ({word})")


class Dispatcher(BaseDispatcher[BaseContext]):
    bot = Bot
    context = BaseContext
    handlers = (Calc, Say, Transfer)

    async def on_error(self, ctx: BaseContext, exc: Exception) -> None:
        # Одно правило на весь бот: неверные аргументы любой команды получают подсказку.
        if isinstance(exc, CommandArgsError):
            await ctx.answer_message(
                f"Не получилось: {exc.problems[0].message}.\nНужно: {exc.usage}"
            )
            return

        await super().on_error(ctx, exc)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s"
    )
    Dispatcher(token=os.environ.get("BOT_TOKEN")).start_polling()
