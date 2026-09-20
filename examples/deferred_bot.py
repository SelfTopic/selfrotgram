import asyncio
import logging
import os

from selfrot import BaseContext, BaseDispatcher, Bot, CommandArgs, MessageHandler, Rest
from selfrot.filter import Command
from selfrot.types import TextMessage

# Отложенные действия: сделать что-то ПОСЛЕ того, как хендлер закончил. Хендлер не ждёт:
# слот диспетчера и сессия БД освобождаются сразу. Таймеры живут в памяти, при
# перезапуске бота пропадают (для важных напоминаний нужна база).

SECRET_TTL = 10  # секунд до самоуничтожения сообщения
REPORT_SECONDS = 3  # сколько «готовится отчёт»


class Secret(MessageHandler[BaseContext[TextMessage]]):
    """/secret: код, который удалится сам."""

    query = Command("secret")

    async def handle(self) -> None:
        sent = await self.ctx.message.reply(f"Код: 1234 (удалю через {SECRET_TTL} с)")
        self.defer(
            sent.delete, delay=SECRET_TTL
        )  # записали, что делать потом; идём дальше


class RemindArgs(CommandArgs):
    seconds: int
    text: Rest


class Remind(MessageHandler[BaseContext[TextMessage]]):
    """/remind 5 позвонить маме: напомнить через 5 секунд."""

    cmd = Command("remind", RemindArgs)
    query = cmd

    async def pre_handle(self) -> None:
        self.args = self.cmd.parse(self.ctx)  # неверные аргументы уйдут в on_error

    async def handle(self) -> None:
        self.reminder = self.defer(self.remind, self.args.text, delay=self.args.seconds)
        await self.ctx.message.reply(f"Напомню через {self.args.seconds} с")

    async def remind(self, text: str) -> None:
        # Выполняется уже после закрытия хендлера. Есть self и self.ctx (бот, апдейт).
        await self.ctx.message.answer(f"⏰ Напоминание: {text}")


class Report(MessageHandler[BaseContext[TextMessage]]):
    """/report: долгая работа. Быстрая часть здесь, долгая в after_handle."""

    query = Command("report")

    async def handle(self) -> None:
        self.processing = await self.ctx.message.reply("⏳ Готовлю отчёт...")
        # handle закончился: слот освобождён, база закоммичена (если она есть)

    async def after_handle(self) -> None:
        await asyncio.sleep(
            REPORT_SECONDS
        )  # тут может быть ожидание задачи или очереди
        await self.processing.edit_text("✅ Отчёт готов")

    async def on_error(self, exc: Exception) -> None:
        # Сюда попадают и ошибки из after_handle.
        await self.ctx.message.answer("❌ Не получилось приготовить отчёт")


class Dispatcher(BaseDispatcher[BaseContext]):
    bot = Bot
    context = BaseContext
    handlers = (Secret, Remind, Report)
    max_deferred = 1000  # сколько отложенных вызовов может жить одновременно

    async def on_error(self, ctx: BaseContext, exc: Exception) -> None:
        # Неверные аргументы /remind: подсказка. Остальное только в лог.
        usage = getattr(exc, "usage", None)
        if usage:
            await ctx.answer_message(f"Нужно: {usage}")
            return

        await super().on_error(ctx, exc)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s"
    )
    Dispatcher(token=os.environ.get("BOT_TOKEN")).start_polling()
