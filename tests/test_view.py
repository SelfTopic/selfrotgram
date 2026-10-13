"""View и Pagination: самообновляющееся сообщение без edit_message_text в хендлере."""

from typing import Any

import pytest

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
from selfrot.exceptions import DefinitionError
from selfrot.filter import Command
from selfrot.handlers import CallbackQueryHandler
from selfrot.keyboard import button
from selfrot.types import (
    DataCallbackQuery,
    InputRichBlockParagraph,
    InputRichMessage,
    TextMessage,
)

from .conftest import TOKEN, FakeTelegram, bind, callback_update, message_update


def ctx(raw: dict[str, Any], api: Bot) -> BaseContext[Any]:
    return BaseContext(bind(raw, api), api)


class TestViewDefinition:
    """Классы View/Pagination никогда не создаются (всё через classmethod), поэтому
    обычная защита ABC от «забыли переопределить» не срабатывает без явной проверки —
    этот блок как раз и проверяет, что явная проверка на месте."""

    def test_forgetting_render_raises_at_class_definition(self):
        with pytest.raises(DefinitionError, match="render"):

            class Broken(View):
                payload = CallbackPayload

    def test_overriding_render_in_an_intermediate_class_is_recognized(self):
        class WithRender(View):
            payload = CallbackPayload

            @classmethod
            async def render(cls, ctx: BaseContext[Any], data: Any) -> ViewContent:
                return ViewContent(body="x")

        class Leaf(WithRender):
            pass  # render унаследован от WithRender, не от View — не должно падать

        assert Leaf.payload is CallbackPayload

    def test_pagination_forgetting_total_raises(self):
        with pytest.raises(DefinitionError, match="total"):

            class Broken(Pagination, prefix="broken-total"):
                @classmethod
                async def page_content(cls, ctx: BaseContext[Any], page: int) -> ViewContent:
                    return ViewContent(body="x")

    def test_pagination_forgetting_page_content_raises(self):
        with pytest.raises(DefinitionError, match="page_content"):

            class Broken(Pagination, prefix="broken-page-content"):
                @classmethod
                async def total(cls, ctx: BaseContext[Any]) -> int:
                    return 1

    def test_pagination_generates_its_own_payload(self):
        class A(Pagination, prefix="payload-a"):
            @classmethod
            async def total(cls, ctx: BaseContext[Any]) -> int:
                return 1

            @classmethod
            async def page_content(cls, ctx: BaseContext[Any], page: int) -> ViewContent:
                return ViewContent(body="x")

        class B(Pagination, prefix="payload-b"):
            total = A.total  # type: ignore[assignment]
            page_content = A.page_content  # type: ignore[assignment]

        assert A.payload is not B.payload  # разные подклассы — разные типы данных кнопки
        assert A.payload.__prefix__ == "payload-a"
        assert B.payload.__prefix__ == "payload-b"


class CounterPress(CallbackPayload, prefix="counter"):
    delta: int


class Counter(View):
    """Минимальный View: состояние в самом classvar, apply() не переопределён (по
    умолчанию ничего не делает) — вся работа в render()."""

    payload = CounterPress
    n: int = 0

    @classmethod
    async def render(cls, ctx: BaseContext[Any], data: CallbackPayload | None) -> ViewContent:
        if isinstance(data, CounterPress):
            cls.n += data.delta
        return ViewContent(
            body=str(cls.n),
            rows=[[button("+1", CounterPress(delta=1)), button("-1", CounterPress(delta=-1))]],
        )


class ShowCounter(MessageHandler[BaseContext[TextMessage]]):
    query = Command("counter")

    async def handle(self) -> None:
        await Counter.show(self.ctx)


class CounterPressed(CallbackQueryHandler[BaseContext[DataCallbackQuery]]):
    query = Counter.filter()

    async def handle(self) -> None:
        await Counter.press(self.ctx)


class CounterDispatcher(BaseDispatcher[BaseContext]):
    bot = Bot
    context = BaseContext
    handlers = (ShowCounter, CounterPressed)


class TestViewEndToEnd:
    @pytest.fixture
    async def dp(self, telegram: FakeTelegram):
        Counter.n = 0  # общий classvar между тестами — сбрасываем
        app = CounterDispatcher(token=TOKEN)
        yield app
        await app.api.close_session()

    async def test_show_sends_and_press_edits_without_touching_telegram_api_in_handler(
        self, telegram: FakeTelegram, dp: CounterDispatcher
    ):
        await dp._handle(dp.create_context(bind(message_update("/counter"), dp.api)))
        assert telegram.methods() == ["sendMessage"]
        assert telegram.sent[-1]["text"] == "0"
        assert telegram.sent[-1]["reply_markup"] == {
            "inline_keyboard": [
                [
                    {"text": "+1", "callback_data": "counter:1"},
                    {"text": "-1", "callback_data": "counter:-1"},
                ]
            ]
        }

        telegram.clear()
        await dp._handle(dp.create_context(bind(callback_update("counter:1"), dp.api)))
        assert telegram.methods() == ["editMessageText", "answerCallbackQuery"]
        edited = telegram.calls[0][1]
        assert edited["text"] == "1"

    async def test_bad_callback_data_just_answers(
        self, telegram: FakeTelegram, dp: CounterDispatcher
    ):
        # Нажатие на чужую кнопку (другой префикс) не подошло бы под query = Counter.filter(),
        # но press() и сам по себе безопасен на мусорных данных.
        c = ctx(callback_update("counter:not-a-number"), dp.api)
        await Counter.press(c)
        assert telegram.methods() == ["answerCallbackQuery"]


class TestPaginationNav:
    ITEMS = [f"Товар {i}" for i in range(1, 23)]

    @staticmethod
    def make(per_page: int = 5, closable: bool = False):
        items = TestPaginationNav.ITEMS

        class Catalog(Pagination, prefix=f"cat-{per_page}-{closable}"):
            @classmethod
            async def total(cls, ctx: BaseContext[Any]) -> int:
                return len(items)

            @classmethod
            async def page_content(cls, ctx: BaseContext[Any], page: int) -> ViewContent:
                start = page * cls.per_page
                return ViewContent(body="\n".join(items[start : start + cls.per_page]))

        Catalog.per_page = per_page
        Catalog.closable = closable
        return Catalog

    async def test_first_page_has_no_prev_button(self, bot: Bot):
        Catalog = self.make()
        content = await Catalog.render(ctx(message_update("/x"), bot), None)
        nav = content.rows[-1]
        assert nav[0].callback_data == f"{Catalog.payload.__prefix__}:noop:0"
        assert nav[1].text == "1/5"
        assert nav[2].callback_data == f"{Catalog.payload.__prefix__}:goto:1"

    async def test_last_page_has_no_next_button(self, bot: Bot):
        Catalog = self.make()
        data = Catalog.payload(action="goto", page=99)  # type: ignore[call-arg]  # дальше края
        content = await Catalog.render(ctx(message_update("/x"), bot), data)
        nav = content.rows[-1]
        assert nav[1].text == "5/5"
        assert nav[2].callback_data == f"{Catalog.payload.__prefix__}:noop:0"

    async def test_requested_page_is_clamped(self, bot: Bot):
        Catalog = self.make()
        page_99 = Catalog.payload(page=99)  # type: ignore[call-arg]
        content = await Catalog.render(ctx(message_update("/x"), bot), page_99)
        assert content.body == "Товар 21\nТовар 22"  # последняя страница, не падает

    async def test_empty_list_still_has_one_page(self, bot: Bot):
        class Empty(Pagination, prefix="empty"):
            @classmethod
            async def total(cls, ctx: BaseContext[Any]) -> int:
                return 0

            @classmethod
            async def page_content(cls, ctx: BaseContext[Any], page: int) -> ViewContent:
                return ViewContent(body="Пусто")

        content = await Empty.render(ctx(message_update("/x"), bot), None)
        assert content.rows[-1][1].text == "1/1"

    async def test_closable_adds_close_button_only_when_enabled(self, bot: Bot):
        without = self.make(closable=False)
        with_close = self.make(closable=True)

        plain = await without.render(ctx(message_update("/x"), bot), None)
        closing = await with_close.render(ctx(message_update("/x"), bot), None)

        assert len(plain.rows[-1]) == 3
        assert len(closing.rows[-1]) == 4
        assert closing.rows[-1][3].text == "✕"

    async def test_item_rows_stay_before_the_nav_row(self, bot: Bot):
        class WithItems(Pagination, prefix="with-items"):
            @classmethod
            async def total(cls, ctx: BaseContext[Any]) -> int:
                return 1

            @classmethod
            async def page_content(cls, ctx: BaseContext[Any], page: int) -> ViewContent:
                return ViewContent(body="x", rows=[[button("пункт", "irrelevant")]])

        content = await WithItems.render(ctx(message_update("/x"), bot), None)
        assert len(content.rows) == 2
        assert content.rows[0][0].text == "пункт"
        assert content.rows[1][1].text == "1/1"  # навигация вторым, последним рядом


class TestPaginationClose:
    async def test_default_close_deletes_the_message(self, telegram: FakeTelegram, bot: Bot):
        class Catalog(Pagination, prefix="close-default"):
            closable = True

            @classmethod
            async def total(cls, ctx: BaseContext[Any]) -> int:
                return 1

            @classmethod
            async def page_content(cls, ctx: BaseContext[Any], page: int) -> ViewContent:
                return ViewContent(body="x")

        c = ctx(callback_update("close-default:close:0"), bot)
        await Catalog.press(c)
        assert telegram.methods() == ["deleteMessage", "answerCallbackQuery"]

    async def test_closed_can_be_overridden(self, telegram: FakeTelegram, bot: Bot):
        closed_calls = []

        class Catalog(Pagination, prefix="close-custom"):
            closable = True

            @classmethod
            async def total(cls, ctx: BaseContext[Any]) -> int:
                return 1

            @classmethod
            async def page_content(cls, ctx: BaseContext[Any], page: int) -> ViewContent:
                return ViewContent(body="x")

            @classmethod
            async def closed(cls, ctx: BaseContext[Any]) -> None:
                closed_calls.append(ctx)
                await ctx.answer_message("Закрыто без удаления")

        c = ctx(callback_update("close-custom:close:0"), bot)
        await Catalog.press(c)
        assert len(closed_calls) == 1
        assert telegram.methods() == ["sendMessage", "answerCallbackQuery"]
        assert telegram.sent[-1]["text"] == "Закрыто без удаления"

    async def test_noop_press_only_answers(self, telegram: FakeTelegram, bot: Bot):
        class Catalog(Pagination, prefix="noop-test"):
            @classmethod
            async def total(cls, ctx: BaseContext[Any]) -> int:
                return 1

            @classmethod
            async def page_content(cls, ctx: BaseContext[Any], page: int) -> ViewContent:
                return ViewContent(body="x")

        c = ctx(callback_update("noop-test:noop:0"), bot)
        await Catalog.press(c)
        assert telegram.methods() == ["answerCallbackQuery"]


class TestRichMessageBody:
    async def test_plain_text_uses_send_and_edit_message_text(
        self, telegram: FakeTelegram, bot: Bot
    ):
        class Plain(Pagination, prefix="rich-plain"):
            @classmethod
            async def total(cls, ctx: BaseContext[Any]) -> int:
                return 1

            @classmethod
            async def page_content(cls, ctx: BaseContext[Any], page: int) -> ViewContent:
                return ViewContent(body="обычный текст")

        await Plain.show(ctx(message_update("/x"), bot))
        assert telegram.methods() == ["sendMessage"]
        assert telegram.sent[-1]["text"] == "обычный текст"
        assert "rich_message" not in telegram.sent[-1]

        telegram.clear()
        c = ctx(callback_update("rich-plain:goto:0"), bot)
        await Plain.press(c)
        assert telegram.methods() == ["editMessageText", "answerCallbackQuery"]
        assert telegram.calls[0][1]["text"] == "обычный текст"

    async def test_rich_body_uses_send_and_edit_rich_message(
        self, telegram: FakeTelegram, bot: Bot
    ):
        rich = InputRichMessage(blocks=[InputRichBlockParagraph(text="таблица")])

        class Rich(Pagination, prefix="rich-body"):
            @classmethod
            async def total(cls, ctx: BaseContext[Any]) -> int:
                return 1

            @classmethod
            async def page_content(cls, ctx: BaseContext[Any], page: int) -> ViewContent:
                return ViewContent(body=rich)

        await Rich.show(ctx(message_update("/x"), bot))
        assert telegram.methods() == ["sendRichMessage"]
        assert telegram.sent == []  # sent — только тела sendMessage, тут другой метод
        assert telegram.calls[0][1]["rich_message"]["blocks"][0]["text"] == "таблица"

        telegram.clear()
        c = ctx(callback_update("rich-body:goto:0"), bot)
        await Rich.press(c)
        assert telegram.methods() == ["editMessageText", "answerCallbackQuery"]
        assert telegram.calls[0][1]["rich_message"]["blocks"][0]["text"] == "таблица"
        assert "text" not in telegram.calls[0][1]
