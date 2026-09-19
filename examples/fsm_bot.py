import logging
import os

from pydantic import BaseModel

from selfrot import (
    BaseContext,
    BaseDispatcher,
    Bot,
    MemoryStorage,
    MessageHandler,
    State,
    States,
)
from selfrot.filter import Command, HasText, InState, NoState, Text
from selfrot.types import TextMessage

# Многошаговый диалог: /form → имя → возраст → подтверждение. Данные каждого шага
# типизированы: fsm.get(Form.age) возвращает AgeStep, а не dict.


class AgeStep(BaseModel):
    name: str


class ConfirmStep(AgeStep):
    age: int


class Form(States):
    name = State()  # данных нет
    age = State(AgeStep)  # данные — модель
    confirm = State(ConfirmStep)


class Start(MessageHandler[BaseContext[TextMessage]]):
    query = Command("form") & NoState()  # начать можно, только если диалога ещё нет

    async def handle(self) -> None:
        await self.ctx.fsm.set(Form.name)
        await self.ctx.message.answer("Как тебя зовут? (/cancel — отмена)")


class Cancel(MessageHandler[BaseContext[TextMessage]]):
    query = Command("cancel") & ~NoState()  # стоит выше шагов: работает на любом

    async def handle(self) -> None:
        await self.ctx.fsm.clear()
        await self.ctx.message.answer("Отменено")


class GotName(MessageHandler[BaseContext[TextMessage]]):
    # InState ничего не гарантирует про поля, поэтому текст берём фильтром HasText.
    query = InState(Form.name) & HasText()

    async def handle(self) -> None:
        await self.ctx.fsm.set(Form.age, AgeStep(name=self.ctx.message.text))
        await self.ctx.message.answer("Сколько тебе лет?")


class GotAge(MessageHandler[BaseContext[TextMessage]]):
    query = InState(Form.age) & HasText()

    async def pre_handle(self) -> None:
        self.age = int(self.ctx.message.text)  # ValueError уходит в on_error

    async def handle(self) -> None:
        previous = await self.ctx.fsm.get(Form.age)  # AgeStep
        await self.ctx.fsm.set(
            Form.confirm, ConfirmStep(name=previous.name, age=self.age)
        )
        await self.ctx.message.answer(
            f"{previous.name}, {self.age}. Всё верно? (да / нет)"
        )

    async def on_error(self, exc: Exception) -> None:
        if isinstance(exc, ValueError):
            await self.ctx.message.answer("Нужно число")
            return

        raise exc


class Confirmed(MessageHandler[BaseContext[TextMessage]]):
    query = InState(Form.confirm) & Text("да", ignore_case=True)

    async def handle(self) -> None:
        data = await self.ctx.fsm.get(Form.confirm)
        await self.ctx.fsm.clear()
        await self.ctx.message.answer(f"Сохранено: {data.name}, {data.age}")


class Declined(MessageHandler[BaseContext[TextMessage]]):
    query = InState(Form.confirm) & Text("нет", ignore_case=True)

    async def handle(self) -> None:
        await self.ctx.fsm.clear()
        await self.ctx.message.answer("Ок, начнём заново: /form")


class Dispatcher(BaseDispatcher[BaseContext]):
    bot = Bot
    context = BaseContext
    # Брошенный диалог сам исчезает через 10 минут.
    fsm_storage = MemoryStorage(ttl=600)
    handlers = (Start, Cancel, GotName, GotAge, Confirmed, Declined)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s"
    )
    Dispatcher(token=os.environ.get("BOT_TOKEN")).start_polling()
