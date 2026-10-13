import logging
import os

from selfrot import (
    BaseContext,
    BaseDispatcher,
    Bot,
    CallbackPayload,
    MessageHandler,
    Pagination,
    View,
    ViewContent,
)
from selfrot.filter import Command
from selfrot.handlers import CallbackQueryHandler
from selfrot.keyboard import button
from selfrot.types import DataCallbackQuery, TextMessage

# View и Pagination: хендлер не видит ни edit_message_text, ни callback_query.answer(),
# ни разбора данных кнопки — всё это делает сам объект, вы пишете только render()
# (как выглядит содержимое сейчас) и, если что-то меняется, apply() (что сделать с
# состоянием до повторного render()).


# --- 1. Pagination: частный случай View с номером страницы -------------------------
# Вместо payload и render() — total() (сколько всего) и page_content() (содержимое
# одной уже зажатой в границы страницы). Навигационный ряд («« N/M »») собирает сама.

ITEMS = [f"Товар {i}" for i in range(1, 23)]


class ItemPayload(CallbackPayload, prefix="item"):
    index: int


class Catalog(Pagination, prefix="catalog"):
    per_page = 5

    @classmethod
    async def total(cls, ctx: BaseContext[TextMessage]) -> int:
        return len(ITEMS)  # тут мог бы быть await ctx.db.count(...)

    @classmethod
    async def page_content(cls, ctx: BaseContext[TextMessage], page: int) -> ViewContent:
        start = page * cls.per_page
        chunk = ITEMS[start : start + cls.per_page]
        # Элементы списка кликабельны: ряд кнопок до навигации, а не просто текст.
        rows = [[button(item, ItemPayload(index=start + i))] for i, item in enumerate(chunk)]
        return ViewContent(body="Выберите товар:", rows=rows)


class ListItems(MessageHandler[BaseContext[TextMessage]]):
    """/list показывает первую страницу."""

    query = Command("list")

    async def handle(self) -> None:
        await Catalog.show(self.ctx)


class CatalogPressed(CallbackQueryHandler[BaseContext[DataCallbackQuery]]):
    """Листание страниц каталога."""

    query = Catalog.filter()

    async def handle(self) -> None:
        await Catalog.press(self.ctx)


class ItemPressed(CallbackQueryHandler[BaseContext[DataCallbackQuery]]):
    """Нажатие на конкретный товар — свой payload, свой фильтр, ничего общего с Catalog."""

    press = ItemPayload.filter()
    query = press

    async def handle(self) -> None:
        data = self.press.parse(self.ctx)
        await self.ctx.callback_query.answer(f"Вы выбрали: {ITEMS[data.index]}", show_alert=True)


# --- 2. View напрямую: не всё динамическое — это листание страниц ------------------
# Счётчик меняет число по кнопке, страниц тут нет вообще. payload свой, apply() не
# переопределён (по умолчанию ничего не делает — состояние целиком в самом payload).


class CounterPress(CallbackPayload, prefix="counter"):
    delta: int


class Counter(View):
    payload = CounterPress
    n = 0  # на весь процесс, для примера; в реальности — своё число на чат/пользователя

    @classmethod
    async def render(cls, ctx: BaseContext[TextMessage], data: CallbackPayload | None) -> ViewContent:
        if isinstance(data, CounterPress):
            cls.n += data.delta

        return ViewContent(
            body=f"Счётчик: {cls.n}",
            rows=[[button("−1", CounterPress(delta=-1)), button("+1", CounterPress(delta=1))]],
        )


class ShowCounter(MessageHandler[BaseContext[TextMessage]]):
    query = Command("counter")

    async def handle(self) -> None:
        await Counter.show(self.ctx)


class CounterPressed(CallbackQueryHandler[BaseContext[DataCallbackQuery]]):
    query = Counter.filter()

    async def handle(self) -> None:
        await Counter.press(self.ctx)


class Dispatcher(BaseDispatcher[BaseContext]):
    bot = Bot
    context = BaseContext
    handlers = (ListItems, CatalogPressed, ItemPressed, ShowCounter, CounterPressed)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s"
    )
    Dispatcher(token=os.environ.get("BOT_TOKEN")).start_polling()
