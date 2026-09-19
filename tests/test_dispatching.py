import asyncio
from contextvars import ContextVar

import pytest

from selfrot import (
    BaseContext,
    BaseDispatcher,
    BaseMiddleware,
    BaseRouter,
    Bot,
    MessageHandler,
)
from selfrot.dispatcher import order_by_chat, order_by_user
from selfrot.dispatcher.runner import UpdateRunner
from selfrot.exceptions import DefinitionError, RouterError
from selfrot.filter import Text

from .conftest import FakeTelegram, bind, callback_update, message_update

log: list[str] = []


@pytest.fixture(autouse=True)
def clean_log():
    log.clear()


async def feed(dp: BaseDispatcher, raw: dict) -> None:
    await dp._handle(dp.create_context(bind(raw, dp.api)))


def make(dispatcher_cls: type[BaseDispatcher]) -> BaseDispatcher:
    return dispatcher_cls(token="1:T")


class Say(MessageHandler[BaseContext]):
    word = "x"

    async def handle(self):
        log.append(f"handle:{self.word}")


def handler(name: str, text: str):
    return type(name, (Say,), {"query": Text(text), "word": name})


class TestRouting:
    async def test_first_matching_handler_wins(self, telegram):
        first, second = handler("first", "a"), handler("second", "a")

        class Root(BaseDispatcher[BaseContext]):
            bot = Bot
            context = BaseContext
            handlers = (first, second)

        await feed(make(Root), message_update("a"))
        assert log == ["handle:first"]

    async def test_own_handlers_before_child_routers(self, telegram):
        own, child = handler("own", "a"), handler("child", "a")

        class Child(BaseRouter[BaseContext]):
            context = BaseContext
            handlers = (child,)

        class Root(BaseDispatcher[BaseContext]):
            bot = Bot
            context = BaseContext
            handlers = (own,)
            routers = (Child,)

        await feed(make(Root), message_update("a"))
        assert log == ["handle:own"]

    async def test_handler_of_wrong_kind_is_skipped(self, telegram):
        class Root(BaseDispatcher[BaseContext]):
            bot = Bot
            context = BaseContext
            handlers = (handler("msg", "a"),)

        await feed(
            make(Root), callback_update("a")
        )  # callback_query, а хендлер про message
        assert log == []

    def test_cycle_in_router_tree(self):
        class A(BaseRouter[BaseContext]):
            context = BaseContext

        class B(BaseRouter[BaseContext]):
            context = BaseContext
            routers = (A,)

        A.routers = (B,)
        with pytest.raises(RouterError, match="Цикл"):
            A()

    def test_not_a_router(self):
        class R(BaseRouter[BaseContext]):
            context = BaseContext
            routers = ("не роутер",)  # type: ignore[assignment]

        with pytest.raises(DefinitionError):
            R()

    def test_used_update_types_feed_allowed_updates(self):
        class Root(BaseDispatcher[BaseContext]):
            bot = Bot
            context = BaseContext
            handlers = (handler("m", "a"),)

        assert make(Root).used_update_types() == {"message"}


class Trace(BaseMiddleware[BaseContext]):
    name = "t"

    async def pre_handle(self) -> bool:
        log.append(f"{self.name}:pre")
        return True

    async def post_handle(self, exc=None):
        log.append(f"{self.name}:post({type(exc).__name__ if exc else None})")


def mw(name: str, **attrs):
    return type(name, (Trace,), {"name": name, **attrs})


class TestMiddlewares:
    async def test_order_is_onion(self, telegram):
        class Root(BaseDispatcher[BaseContext]):
            bot = Bot
            context = BaseContext
            middlewares = (mw("outer"), mw("inner"))
            handlers = (handler("h", "a"),)

        await feed(make(Root), message_update("a"))
        assert log == [
            "outer:pre",
            "inner:pre",
            "handle:h",
            "inner:post(None)",
            "outer:post(None)",
        ]

    async def test_dispatcher_middleware_runs_without_handler_router_middleware_does_not(
        self, telegram
    ):
        class Child(BaseRouter[BaseContext]):
            context = BaseContext
            middlewares = (mw("router"),)
            handlers = (handler("h", "a"),)

        class Root(BaseDispatcher[BaseContext]):
            bot = Bot
            context = BaseContext
            middlewares = (mw("dp"),)
            routers = (Child,)

        await feed(make(Root), message_update("нет такого"))
        assert log == ["dp:pre", "dp:post(None)"]

    async def test_pre_handle_false_blocks_handler(self, telegram):
        class Deny(Trace):
            async def pre_handle(self) -> bool:
                log.append("deny")
                return False

        class Root(BaseDispatcher[BaseContext]):
            bot = Bot
            context = BaseContext
            middlewares = (mw("outer"), Deny)
            handlers = (handler("h", "a"),)

        await feed(make(Root), message_update("a"))
        assert log == ["outer:pre", "deny", "outer:post(None)"]

    async def test_failing_pre_handle_still_closes_earlier_middlewares(self, telegram):
        class Boom(Trace):
            async def pre_handle(self) -> bool:
                log.append("boom:pre")
                raise RuntimeError("pre упал")

        class Root(BaseDispatcher[BaseContext]):
            bot = Bot
            context = BaseContext
            middlewares = (mw("db"), Boom)
            handlers = (handler("h", "a"),)

            async def on_error(self, ctx, exc):
                log.append(f"on_error:{exc}")

        await feed(make(Root), message_update("a"))
        assert log == [
            "db:pre",
            "boom:pre",
            "db:post(RuntimeError)",
            "on_error:pre упал",
        ]

    async def test_contextvar_set_in_pre_handle_is_visible_to_handler(self, telegram):
        # На этом держится DI с сессией БД в ContextVar (как у chestor_bot).
        session: ContextVar[str] = ContextVar("session")

        class Db(Trace):
            async def pre_handle(self) -> bool:
                self.token = session.set(f"session-{self.ctx.update.update_id}")
                return True

            async def post_handle(self, exc=None):
                session.reset(self.token)  # в другом контексте это упало бы ValueError

        class Read(Say):
            query = Text("a")

            async def handle(self):
                log.append(session.get())

        class Root(BaseDispatcher[BaseContext]):
            bot = Bot
            context = BaseContext
            middlewares = (Db,)
            handlers = (Read,)

        await feed(make(Root), message_update("a"))
        assert log == ["session-1"]


class Fail(Say):
    query = Text("x")
    boom: Exception = RuntimeError("баг")

    async def handle(self):
        raise self.boom


class TestErrors:
    def dispatcher(self, handler_cls) -> BaseDispatcher:
        class Root(BaseDispatcher[BaseContext]):
            bot = Bot
            context = BaseContext
            middlewares = (mw("db"),)
            handlers = (handler_cls,)

            async def on_error(self, ctx, exc):
                log.append(f"dispatcher:{type(exc).__name__}")

        return make(Root)

    async def test_default_handler_on_error_passes_error_up(self, telegram):
        await feed(self.dispatcher(Fail), message_update("x"))
        assert log == ["db:pre", "db:post(RuntimeError)", "dispatcher:RuntimeError"]

    async def test_handler_on_error_can_handle_and_sees_pre_handle_state(
        self, telegram
    ):
        class Guarded(Fail):
            async def pre_handle(self):
                self.seen = "state"
                raise ValueError("нельзя")

            async def on_error(self, exc):
                if isinstance(exc, ValueError):
                    log.append(f"handled:{exc}:{self.seen}")
                    return
                raise exc

        await feed(self.dispatcher(Guarded), message_update("x"))
        # мидлвари закрылись (откат) до on_error, handle не вызывался
        assert log == ["db:pre", "db:post(ValueError)", "handled:нельзя:state"]

    async def test_unhandled_kind_goes_to_dispatcher(self, telegram):
        class Picky(Fail):
            boom = KeyError("k")

            async def on_error(self, exc):
                if isinstance(exc, ValueError):
                    return
                raise exc

        await feed(self.dispatcher(Picky), message_update("x"))
        assert log[-1] == "dispatcher:KeyError"

    async def test_failing_on_error_does_not_stop_the_bot(self, telegram):
        class Broken(Fail):
            async def on_error(self, exc):
                raise KeyError("сам on_error сломан")

        await feed(self.dispatcher(Broken), message_update("x"))
        assert log[-1] == "dispatcher:KeyError"

    async def test_cancellation_is_not_an_error(self, telegram):
        class Cancelled(Fail):
            boom = asyncio.CancelledError()

            async def on_error(self, exc):
                log.append("on_error вызван")

        with pytest.raises(asyncio.CancelledError):
            await feed(self.dispatcher(Cancelled), message_update("x"))
        assert "on_error вызван" not in log
        assert "db:post(CancelledError)" in log


class TestRunner:
    async def test_different_keys_run_in_parallel(self):
        runner = UpdateRunner(10, 5)
        started = asyncio.get_running_loop().time()

        async def work():
            await asyncio.sleep(0.2)

        for key in range(5):
            await runner.submit(key, work)
        await runner.drain()
        assert asyncio.get_running_loop().time() - started < 0.6

    async def test_same_key_runs_in_order_even_after_failure(self):
        runner = UpdateRunner(10, 5)
        events: list[str] = []

        def job(name: str, delay: float, boom: bool = False):
            async def work():
                events.append(f"start {name}")
                await asyncio.sleep(delay)
                events.append(f"end {name}")
                if boom:
                    raise RuntimeError

            return work

        await runner.submit("a", job("1", 0.1, boom=True))
        await runner.submit("a", job("2", 0.05))
        await runner.submit("a", job("3", 0))
        await runner.drain()
        assert events == ["start 1", "end 1", "start 2", "end 2", "start 3", "end 3"]

    async def test_limit_and_backpressure(self):
        runner = UpdateRunner(2, 5)
        running = peak = 0

        async def work():
            nonlocal running, peak
            running += 1
            peak = max(peak, running)
            await asyncio.sleep(0.1)
            running -= 1

        for key in range(6):
            await runner.submit(key, work)  # submit ждёт свободный слот
        await runner.drain()
        assert peak == 2

    async def test_try_submit_does_not_wait(self):
        runner = UpdateRunner(1, 5)

        async def work():
            await asyncio.sleep(0.1)

        assert await runner.try_submit(1, work)
        assert not await runner.try_submit(2, work)
        await runner.drain()
        assert await runner.try_submit(3, work)
        await runner.drain()

    async def test_drain_waits_then_cancels(self):
        runner = UpdateRunner(10, 0.3)
        cancelled = []
        finished = []

        async def quick():
            await asyncio.sleep(0.1)
            finished.append(1)

        async def stubborn():
            try:
                await asyncio.sleep(5)
            except asyncio.CancelledError:
                cancelled.append(1)
                raise

        await runner.submit(1, quick)
        await runner.submit(2, stubborn)
        await runner.drain()
        assert finished == [1]
        assert cancelled == [1]

    async def test_cancelling_a_waiter_does_not_cancel_the_previous(self):
        runner = UpdateRunner(10, 5)
        done = []

        async def first():
            await asyncio.sleep(0.1)
            done.append("first")

        async def second():
            done.append("second")

        await runner.submit("z", first)
        await runner.submit("z", second)
        runner._tails["z"].cancel()
        await runner.drain()
        assert done == ["first"]

    async def test_slots_are_released_after_errors(self):
        runner = UpdateRunner(2, 5)

        async def boom():
            raise RuntimeError

        for _ in range(10):
            await runner.submit("e", boom)
        await runner.drain()
        assert runner.active == 0


class TestOrdering:
    def test_default_is_no_ordering(self):
        class Root(BaseDispatcher[BaseContext]):
            bot = Bot
            context = BaseContext

        dp = make(Root)
        ctx = dp.create_context(bind(message_update("x"), None))
        assert dp.ordering_key(ctx) is None

    def test_order_by_chat_and_user(self):
        api = Bot("1:T")
        in_group = BaseContext(bind(message_update("x", uid=7, chat=-5), api), api)
        inline = BaseContext(
            bind(
                {
                    "update_id": 1,
                    "inline_query": {
                        "id": "1",
                        "from": {"id": 7, "is_bot": False, "first_name": "u"},
                        "query": "q",
                        "offset": "",
                    },
                },
                api,
            ),
            api,
        )
        assert order_by_chat(in_group) == -5
        assert order_by_chat(inline) == 7  # без чата — пользователь
        assert order_by_user(in_group) == 7

    async def test_same_chat_updates_run_concurrently_by_default_and_in_order_when_asked(
        self, telegram
    ):
        async def run(ordered: bool) -> int:
            active = peak = 0

            class Slow(Say):
                query = Text("x")

                async def handle(self):
                    nonlocal active, peak
                    active += 1
                    peak = max(peak, active)
                    await asyncio.sleep(0.05)
                    active -= 1

            class Root(BaseDispatcher[BaseContext]):
                bot = Bot
                context = BaseContext
                handlers = (Slow,)

                def ordering_key(self, ctx):
                    return order_by_chat(ctx) if ordered else None

            dp = make(Root)
            for _ in range(3):
                await dp.feed_update(bind(message_update("x", chat=-1), dp.api))
            await dp._runner.drain()
            await dp.api.close_session()
            return peak

        assert await run(ordered=False) == 3
        assert await run(ordered=True) == 1


class TestPollingLifecycle:
    async def test_survives_getupdates_failure_and_handler_error(
        self, telegram: FakeTelegram
    ):
        polls = []

        def get_updates(body):
            polls.append(body)
            if len(polls) == 1:
                from aiohttp import web

                return web.Response(text="<html>502</html>", status=502)
            if len(polls) == 2:
                return [
                    message_update("boom") | {"update_id": 10},
                    message_update("hello") | {"update_id": 11},
                ]
            return []

        telegram.on("getUpdates", get_updates)

        class Boom(Say):
            query = Text("boom")

            async def handle(self):
                raise RuntimeError("хендлер упал")

        class Root(BaseDispatcher[BaseContext]):
            bot = Bot
            context = BaseContext
            handlers = (Boom, handler("hello", "hello"))
            polling_timeout = 0

            async def on_startup(self):
                log.append("startup")

            async def on_shutdown(self):
                log.append("shutdown")

        dp = make(Root)
        task = asyncio.create_task(dp.polling())
        await asyncio.sleep(3.5)  # 1 с паузы после 502, дальше апдейты
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task

        assert "handle:hello" in log  # упавший хендлер не остановил бота
        assert log[0] == "startup"
        assert log[-1] == "shutdown"
        assert polls[0]["allowed_updates"] == ["message"]
        assert dp.api.session.session is None  # сессия закрыта при остановке
