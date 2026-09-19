from typing import ClassVar

import pytest
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
from selfrot.exceptions import ContextError, DefinitionError, FSMError
from selfrot.filter import Command, HasText, InState, NoState, Text
from selfrot.fsm import FSM, StoredState

from .conftest import FakeTelegram, bind, message_update


class AgeStep(BaseModel):
    name: str


class ConfirmStep(AgeStep):
    age: int


class Register(States):
    name = State()
    age = State(AgeStep)
    confirm = State(ConfirmStep)


class Other(States):
    name = State()


class Clock:
    def __init__(self) -> None:
        self.now = 0.0

    def __call__(self) -> float:
        return self.now


class TestStates:
    def test_names_include_module_and_group(self):
        assert Register.age.name.endswith("Register:age")
        assert Register.name.name != Other.name.name

    def test_all_lists_group_states_in_order(self):
        assert [s.name.split(":")[1] for s in Register.all()] == [
            "name",
            "age",
            "confirm",
        ]

    def test_state_outside_states_is_rejected(self):
        # До Python 3.12 исключение из __set_name__ приходит обёрнутым в RuntimeError
        # (DefinitionError лежит в __cause__), с 3.12 — как есть.
        with pytest.raises((DefinitionError, RuntimeError)) as info:

            class Bad:
                x = State()

        error = info.value
        assert isinstance(
            error if isinstance(error, DefinitionError) else error.__cause__,
            DefinitionError,
        )


class TestFSM:
    async def test_typed_data_roundtrip(self):
        fsm = FSM(MemoryStorage(), "1:2")
        assert await fsm.state() is None

        await fsm.set(Register.name)
        assert await fsm.state() == Register.name.name

        await fsm.set(Register.age, AgeStep(name="Вася"))
        data = await fsm.get(Register.age)
        assert isinstance(data, AgeStep)
        assert data.name == "Вася"

    async def test_data_accumulates_via_subclass(self):
        fsm = FSM(MemoryStorage(), "k")
        await fsm.set(Register.confirm, ConfirmStep(name="Вася", age=30))
        data = await fsm.get(Register.confirm)
        assert (data.name, data.age) == ("Вася", 30)

    async def test_clear(self):
        fsm = FSM(MemoryStorage(), "k")
        await fsm.set(Register.name)
        await fsm.clear()
        assert await fsm.state() is None

    @pytest.mark.parametrize(
        "action",
        [
            lambda fsm: fsm.get(Register.age),  # сейчас другое состояние
            lambda fsm: fsm.set(
                Register.name, AgeStep(name="x")
            ),  # данные там, где их нет
            lambda fsm: fsm.set(Register.age),  # нет данных там, где они нужны
            lambda fsm: fsm.set(Register.confirm, AgeStep(name="x")),  # не та модель
        ],
    )
    async def test_misuse_raises(self, action):
        fsm = FSM(MemoryStorage(), "k")
        await fsm.set(Register.name)
        with pytest.raises(FSMError):
            await action(fsm)

    async def test_stored_data_not_matching_model(self):
        storage = MemoryStorage()
        await storage.save("k", StoredState(Register.age.name, {"нет": "поля"}))
        with pytest.raises(FSMError):
            await FSM(storage, "k").get(Register.age)

    async def test_no_key_reads_none_but_cannot_write(self):
        fsm = FSM(MemoryStorage(), None)
        assert await fsm.state() is None
        with pytest.raises(FSMError):
            await fsm.set(Register.name)

    def test_context_outside_dispatcher_has_no_fsm(self):
        ctx = BaseContext(bind(message_update("x"), None), Bot("1:T"))
        with pytest.raises(ContextError):
            _ = ctx.fsm


class TestMemoryStorageTTL:
    async def test_expires_and_set_extends(self):
        clock = Clock()
        fsm = FSM(MemoryStorage(ttl=10, clock=clock), "k")
        await fsm.set(Register.name)

        clock.now = 9
        assert await fsm.state() == Register.name.name
        clock.now = 10
        assert await fsm.state() is None

        clock.now = 0
        await fsm.set(Register.name)
        clock.now = 8
        await fsm.set(Register.name)  # скользящее окно
        clock.now = 15
        assert await fsm.state() == Register.name.name

    async def test_forgotten_dialogs_are_swept(self):
        clock = Clock()
        storage = MemoryStorage(ttl=10, clock=clock)
        for i in range(50):
            await FSM(storage, f"u{i}").set(Register.name)

        clock.now = 30
        await FSM(storage, "new").set(Register.name)
        assert len(storage) == 1


class Dialog(BaseDispatcher[BaseContext]):
    bot = Bot
    context = BaseContext
    fsm_storage = MemoryStorage(ttl=600)
    saved: ClassVar[list[tuple[int, str, int]]] = []


class Start(MessageHandler[BaseContext]):
    query = Command("register")

    async def handle(self):
        await self.ctx.fsm.set(Register.name)
        await self.ctx.message.answer("Как тебя зовут?")


class GotName(MessageHandler[BaseContext]):
    query = InState(Register.name) & HasText()

    async def handle(self):
        await self.ctx.fsm.set(Register.age, AgeStep(name=self.ctx.message.text))
        await self.ctx.message.answer("Сколько лет?")


class GotAge(MessageHandler[BaseContext]):
    query = InState(Register.age) & HasText()

    async def pre_handle(self):
        self.age = int(self.ctx.message.text)

    async def handle(self):
        prev = await self.ctx.fsm.get(Register.age)
        await self.ctx.fsm.set(
            Register.confirm, ConfirmStep(name=prev.name, age=self.age)
        )
        await self.ctx.message.answer(f"{prev.name}, {self.age}: верно?")

    async def on_error(self, exc):
        if isinstance(exc, ValueError):
            await self.ctx.message.answer("Нужно число")
            return
        raise exc


class Confirm(MessageHandler[BaseContext]):
    query = InState(Register.confirm) & Text("да", ignore_case=True)

    async def handle(self):
        data = await self.ctx.fsm.get(Register.confirm)
        Dialog.saved.append((self.ctx.user.id, data.name, data.age))
        await self.ctx.fsm.clear()
        await self.ctx.message.answer("Сохранено")


class Cancel(MessageHandler[BaseContext]):
    query = Command("cancel") & ~NoState()

    async def handle(self):
        await self.ctx.fsm.clear()
        await self.ctx.message.answer("Отменено")


class NothingToCancel(MessageHandler[BaseContext]):
    query = Command("cancel")

    async def handle(self):
        await self.ctx.message.answer("Отменять нечего")


class Greeting(MessageHandler[BaseContext]):
    query = NoState() & Text("привет")

    async def handle(self):
        await self.ctx.message.answer("и тебе привет")


Dialog.handlers = (Start, Cancel, NothingToCancel, GotName, GotAge, Confirm, Greeting)


class TestDialogEndToEnd:
    @pytest.fixture
    async def say(self, telegram: FakeTelegram):
        Dialog.saved = []
        dp = Dialog(token="1:T")

        async def send(text: str, uid: int = 7, chat: int | None = None) -> list[str]:
            telegram.clear()
            update = bind(message_update(text, uid=uid, chat=chat), dp.api)
            await dp._handle(dp.create_context(update))
            return [body["text"] for body in telegram.sent]

        yield send
        await dp.api.close_session()

    async def test_full_dialog(self, say):
        assert await say("привет") == ["и тебе привет"]
        assert await say("/register") == ["Как тебя зовут?"]
        assert await say("привет") == ["Сколько лет?"]  # в диалоге это уже ответ на шаг
        assert await say("много") == ["Нужно число"]  # ошибка шага, состояние держится
        assert await say("30") == ["привет, 30: верно?"]
        assert await say("не знаю") == []
        assert await say("Да") == ["Сохранено"]
        assert Dialog.saved == [(7, "привет", 30)]
        assert await say("привет") == ["и тебе привет"]

    async def test_cancel(self, say):
        assert await say("/cancel") == ["Отменять нечего"]
        await say("/register")
        assert await say("/cancel") == ["Отменено"]
        assert await say("привет") == ["и тебе привет"]

    async def test_users_are_isolated(self, say):
        await say("/register", uid=1)
        assert await say("привет", uid=2) == ["и тебе привет"]

    async def test_default_key_is_chat_and_user(self, say):
        await say("/register", uid=7, chat=-100)
        assert await say("привет", uid=8, chat=-100) == [
            "и тебе привет"
        ]  # другой участник
        assert await say("привет", uid=7, chat=-200) == ["и тебе привет"]  # другой чат

    async def test_dispatchers_do_not_share_default_storage(self):
        class A(BaseDispatcher[BaseContext]):
            bot = Bot
            context = BaseContext

        first, second = A(token="1:T"), A(token="1:T")
        assert first._fsm_storage is not second._fsm_storage
