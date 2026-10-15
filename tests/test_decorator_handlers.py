"""
Диспетчеризация декораторами внутри одного хендлера: несколько методов, каждый
украшен фильтром как декоратором (`@query async def имя(self): ...`), вместо
отдельного класса на каждую ветку. См. docstring BaseHandler.
"""

from enum import Enum

import pytest

from selfrot import BaseContext, BaseDispatcher, Bot, CallbackPayload, CommandArgs, MessageHandler, Rest
from selfrot.exceptions import DefinitionError
from selfrot.filter import Command, HasReplyUser, HasUser
from selfrot.handlers import CallbackQueryHandler
from selfrot.types import DataCallbackQuery, TextMessage, UserMessage

from .conftest import FakeTelegram, bind, callback_update, message_update


async def feed(dp: BaseDispatcher, raw: dict) -> None:
    await dp._handle(dp.create_context(bind(raw, dp.api)))


def make(dispatcher_cls: type[BaseDispatcher]) -> BaseDispatcher:
    return dispatcher_cls(token="1:T")


class FunCommandsEnum(str, Enum):
    choice = "выбери"
    who = "кто"


class FunArgs(CommandArgs):
    command: FunCommandsEnum
    rest: Rest = ""


cmd = Command("fun", FunArgs)


class FunHandler(MessageHandler[BaseContext[TextMessage]]):
    @cmd.where(command=FunCommandsEnum.choice) & HasReplyUser()
    async def choice_reply(self):
        offender = self.ctx.message.reply_to_message.user
        await self.ctx.message.reply(f"Выбираю {offender.first_name}!")

    @cmd.where(command=FunCommandsEnum.choice) & ~HasReplyUser()
    async def choice(self):
        await self.ctx.message.reply("Выбираю... случайного участника чата!")

    @cmd.where(command=FunCommandsEnum.who)
    async def who(self):
        await self.ctx.message.reply("Случайный участник: вот ты!")


class TestMessageHandlerBranches:
    def dispatcher(self) -> BaseDispatcher:
        class Root(BaseDispatcher[BaseContext]):
            bot = Bot
            context = BaseContext
            handlers = (FunHandler,)

        return make(Root)

    async def test_branch_with_combinator_matches_first(self, telegram: FakeTelegram):
        reply = {
            "message_id": 5,
            "date": 1,
            "chat": {"id": 7, "type": "private", "first_name": "В"},
            "text": "привет",
            "from": {"id": 99, "is_bot": False, "first_name": "Петя"},
        }
        await feed(self.dispatcher(), message_update("/fun выбери", reply_to_message=reply))
        assert telegram.sent[-1]["text"] == "Выбираю Петя!"

    async def test_branch_with_negated_combinator_matches(self, telegram: FakeTelegram):
        await feed(self.dispatcher(), message_update("/fun выбери"))
        assert telegram.sent[-1]["text"] == "Выбираю... случайного участника чата!"

    async def test_branch_without_combinator_matches(self, telegram: FakeTelegram):
        await feed(self.dispatcher(), message_update("/fun кто"))
        assert telegram.sent[-1]["text"] == "Случайный участник: вот ты!"

    async def test_no_branch_matches_update_falls_through(self, telegram: FakeTelegram):
        await feed(self.dispatcher(), message_update("/fun ерунда"))
        assert telegram.sent == []


class QuizAnswer(CallbackPayload, prefix="quiz"):
    question_id: int
    option: int


class QuizPressed(CallbackQueryHandler[BaseContext[DataCallbackQuery]]):
    @QuizAnswer.filter(option=0)
    async def gul(self):
        await self.ctx.callback_query.answer("Ты выбрал: Гуль", show_alert=True)

    @QuizAnswer.filter(option=1)
    async def human(self):
        await self.ctx.callback_query.answer("Ты выбрал: Человек", show_alert=True)


class TestCallbackQueryHandlerBranches:
    """Тот же механизм работает для любого вида хендлера, не только MessageHandler."""

    def dispatcher(self) -> BaseDispatcher:
        class Root(BaseDispatcher[BaseContext]):
            bot = Bot
            context = BaseContext
            handlers = (QuizPressed,)

        return make(Root)

    async def test_first_option_branch(self, telegram: FakeTelegram):
        await feed(self.dispatcher(), callback_update("quiz:1:0"))
        _, body = next(c for c in telegram.calls if c[0] == "answerCallbackQuery")
        assert body["text"] == "Ты выбрал: Гуль"

    async def test_second_option_branch(self, telegram: FakeTelegram):
        await feed(self.dispatcher(), callback_update("quiz:1:1"))
        _, body = next(c for c in telegram.calls if c[0] == "answerCallbackQuery")
        assert body["text"] == "Ты выбрал: Человек"

    async def test_unmatched_option_falls_through(self, telegram: FakeTelegram):
        # Ни одна ветка не подошла — апдейт не достался ни одному хендлеру, но
        # дефолтный on_unhandled_callback всё равно закрывает «часики» на кнопке.
        await feed(self.dispatcher(), callback_update("quiz:1:99"))
        assert telegram.calls == [("answerCallbackQuery", {"callback_query_id": "cq1"})]


class TestDefinitionErrors:
    def test_two_decorators_on_one_method(self):
        with pytest.raises(DefinitionError, match="два декоратора-фильтра"):

            class X(MessageHandler[BaseContext[TextMessage]]):
                @cmd.where(command=FunCommandsEnum.who)
                @cmd.where(command=FunCommandsEnum.choice)
                async def one(self): ...

    def test_mixing_query_and_decorators(self):
        with pytest.raises(DefinitionError, match="нельзя смешивать query и методы-декораторы"):

            class X(MessageHandler[BaseContext[TextMessage]]):
                query = cmd

                @cmd.where(command=FunCommandsEnum.who)
                async def who(self): ...

    def test_decorators_with_own_handle(self):
        with pytest.raises(DefinitionError, match="нельзя писать handle"):

            class X(MessageHandler[BaseContext[TextMessage]]):
                @cmd.where(command=FunCommandsEnum.who)
                async def who(self): ...

                async def handle(self): ...

    def test_completely_empty_handler(self):
        with pytest.raises(DefinitionError, match="хендлер пуст"):

            class X(MessageHandler[BaseContext[TextMessage]]):
                pass

    def test_query_without_handle_is_also_empty(self):
        # Раньше это ловил @abstractmethod на handle(); теперь handle() есть
        # по умолчанию (диспетчеризация по декораторам), так что забытый handle()
        # при классическом query нужно ловить явно.
        with pytest.raises(DefinitionError, match="хендлер пуст"):

            class X(MessageHandler[BaseContext[TextMessage]]):
                query = cmd

    def test_header_wider_than_branches_guarantee(self):
        with pytest.raises(DefinitionError, match="не гарантируют поля"):

            class X(MessageHandler[BaseContext[UserMessage]]):
                @cmd.where(command=FunCommandsEnum.who)
                async def who(self): ...

    def test_adding_missing_combinator_fixes_header_mismatch(self):
        class X(MessageHandler[BaseContext[UserMessage]]):
            @cmd.where(command=FunCommandsEnum.who) & HasUser()
            async def who(self): ...

        assert [name for _, name, _ in X._entries] == ["who"]

    def test_classic_style_is_unaffected(self):
        class X(MessageHandler[BaseContext[TextMessage]]):
            query = cmd

            async def handle(self): ...

        assert X.query is cmd


class RepliedTargetMixin:
    """Как RepliedTargetHandler у chestor_bot: миксин не наследует BaseHandler вовсе,
    держит handle(), финальный класс добавляет query и переопределяет perform()."""

    async def perform(self) -> str:
        raise NotImplementedError

    async def handle(self) -> None:
        await self.perform()


class TestHandleFromMixin:
    """handle() пришёл от миксина (не от самого класса и не от BaseHandler) — обычный
    приём композиции, не тот же механизм, что декораторы-ветки, и не должен путаться
    с ним: query+handle-от-миксина — валидный классический стиль."""

    async def test_query_plus_mixin_handle_is_valid(self, telegram: FakeTelegram):
        calls = []

        class Perform(RepliedTargetMixin):
            async def perform(self) -> None:
                calls.append("called")

        class X(Perform, MessageHandler[BaseContext[TextMessage]]):
            query = cmd

        class Root(BaseDispatcher[BaseContext]):
            bot = Bot
            context = BaseContext
            handlers = (X,)

        await feed(make(Root), message_update("/fun"))
        assert calls == ["called"]

    def test_mixin_handle_without_query_is_still_empty(self):
        # Миксин без handle() вообще (только perform, который сам ничего не вызывает) —
        # не считается: пустой хендлер должен падать, как и раньше.
        with pytest.raises(DefinitionError, match="хендлер пуст"):

            class X(MessageHandler[BaseContext[TextMessage]]):
                async def perform(self) -> None: ...

    def test_decorators_with_handle_from_mixin(self):
        with pytest.raises(DefinitionError, match="нельзя писать handle"):

            class X(RepliedTargetMixin, MessageHandler[BaseContext[TextMessage]]):
                @cmd.where(command=FunCommandsEnum.who)
                async def who(self): ...
