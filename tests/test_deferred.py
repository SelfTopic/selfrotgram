import asyncio
from contextvars import ContextVar

import pytest

from selfrot import BaseContext, BaseDispatcher, BaseMiddleware, Bot, MessageHandler
from selfrot.exceptions import ContextError, DeferredLimitError, DefinitionError
from selfrot.filter import Text

from .conftest import bind, message_update

log: list[str] = []


@pytest.fixture(autouse=True)
def clean_log():
    log.clear()


class Trace(BaseMiddleware[BaseContext]):
    async def pre_handle(self) -> bool:
        log.append("mw:pre")
        return True

    async def post_handle(self, exc=None):
        log.append(f"mw:post({type(exc).__name__ if exc else None})")


async def note(text: str) -> None:
    log.append(text)


async def boom() -> None:
    raise RuntimeError("отложенное упало")


def dispatcher(*handlers, **attrs) -> BaseDispatcher:
    class Root(BaseDispatcher[BaseContext]):
        bot = Bot
        context = BaseContext
        middlewares = (Trace,)

        async def on_error(self, ctx, exc):
            log.append(f"dispatcher.on_error:{type(exc).__name__}:{exc}")

    Root.handlers = handlers
    for name, value in attrs.items():
        setattr(Root, name, value)

    return Root(token="1:T")


async def feed(dp: BaseDispatcher, text: str = "go") -> None:
    await dp._handle(dp.create_context(bind(message_update(text), dp.api)))


async def settle(dp: BaseDispatcher, timeout: float = 2.0) -> None:
    """Дождаться, пока отложенные вызовы закончатся."""
    async with asyncio.timeout(timeout):
        while dp._background.active:
            await asyncio.sleep(0.01)


class Go(MessageHandler[BaseContext]):
    query = Text("go")

    async def handle(self):
        pass


def make(name: str, **methods):
    return type(name, (Go,), methods)


class TestDefer:
    async def test_runs_after_delay_not_before(self, telegram):
        async def handle(self):
            self.defer(note, "позже", delay=0.15)
            log.append("handle")

        dp = dispatcher(make("H", handle=handle))
        started = asyncio.get_running_loop().time()
        await feed(dp)
        assert asyncio.get_running_loop().time() - started < 0.1  # хендлер не ждал
        assert log == ["mw:pre", "handle", "mw:post(None)"]  # отложенное ещё спит

        await settle(dp)
        assert log[-1] == "позже"
        assert asyncio.get_running_loop().time() - started >= 0.14

    async def test_starts_after_middlewares_closed(self, telegram):
        async def handle(self):
            self.defer(note, "deferred")  # delay=0: сразу, но всё равно после закрытия

        dp = dispatcher(make("H", handle=handle))
        await feed(dp)
        await settle(dp)
        assert log == ["mw:pre", "mw:post(None)", "deferred"]

    async def test_arguments_and_keywords_are_passed(self, telegram):
        async def record(a, b, *, c):
            log.append(f"{a}{b}{c}")

        async def handle(self):
            self.defer(record, 1, 2, c=3)

        dp = dispatcher(make("H", handle=handle))
        await feed(dp)
        await settle(dp)
        assert log[-1] == "123"

    async def test_dropped_when_handler_fails(self, telegram):
        async def handle(self):
            self.defer(note, "не должно выполниться")
            raise ValueError("хендлер упал")

        dp = dispatcher(make("H", handle=handle))
        await feed(dp)
        await asyncio.sleep(0.1)
        assert "не должно выполниться" not in log
        assert dp._background.active == 0  # место в лимите освобождено

    async def test_dropped_even_if_handler_on_error_handled_the_failure(self, telegram):
        async def handle(self):
            self.defer(note, "не должно выполниться")
            raise ValueError("упал")

        async def on_error(self, exc):
            log.append("handled")

        dp = dispatcher(make("H", handle=handle, on_error=on_error))
        await feed(dp)
        await asyncio.sleep(0.1)
        assert "handled" in log
        assert "не должно выполниться" not in log

    async def test_bound_method_of_the_handler(self, telegram):
        async def later(self, value):
            log.append(f"later:{value}:{self.ctx.user.id}")

        async def handle(self):
            self.defer(self.later, "x")

        dp = dispatcher(make("H", handle=handle, later=later))
        await feed(dp)
        await settle(dp)
        assert log[-1] == "later:x:7"

    async def test_cancel_before_and_after_start(self, telegram):
        handles = []

        async def handle(self):
            handles.append(self.defer(note, "отменённое", delay=0.3))
            handles.append(self.defer(note, "второе", delay=0.3))
            handles[0].cancel()  # до старта

        dp = dispatcher(make("H", handle=handle))
        await feed(dp)
        await asyncio.sleep(0.05)
        handles[1].cancel()  # во время задержки
        await settle(dp)
        assert "отменённое" not in log
        assert "второе" not in log
        assert handles[0].cancelled and handles[1].cancelled

    async def test_sync_function_and_negative_delay_are_rejected(self, telegram):
        errors = []

        async def handle(self):
            for call in (
                lambda: self.defer(print),
                lambda: self.defer(note, "x", delay=-1),
            ):
                try:
                    call()
                except DefinitionError as e:
                    errors.append(str(e))

        dp = dispatcher(make("H", handle=handle))
        await feed(dp)
        assert len(errors) == 2

    async def test_context_without_dispatcher(self):
        ctx = BaseContext(bind(message_update("x"), None), Bot("1:T"))
        with pytest.raises(ContextError):
            ctx.defer(note, "x")


class TestAfterHandle:
    async def test_runs_after_close_with_handler_state(self, telegram):
        async def handle(self):
            self.value = "из handle"
            log.append("handle")

        async def after_handle(self):
            log.append(f"after:{self.value}")

        dp = dispatcher(make("H", handle=handle, after_handle=after_handle))
        await feed(dp)
        await settle(dp)
        assert log == ["mw:pre", "handle", "mw:post(None)", "after:из handle"]

    async def test_not_run_when_handler_fails(self, telegram):
        async def handle(self):
            raise ValueError

        async def after_handle(self):
            log.append("after")

        dp = dispatcher(make("H", handle=handle, after_handle=after_handle))
        await feed(dp)
        await asyncio.sleep(0.1)
        assert "after" not in log

    async def test_error_goes_to_handler_on_error_then_dispatcher(self, telegram):
        async def after_handle(self):
            raise KeyError("k")

        async def on_error(self, exc):
            if isinstance(exc, ValueError):
                return
            raise exc

        dp = dispatcher(make("H", after_handle=after_handle, on_error=on_error))
        await feed(dp)
        await settle(dp)
        assert log[-1].startswith("dispatcher.on_error:KeyError")

    async def test_error_handled_by_handler_on_error(self, telegram):
        async def after_handle(self):
            raise ValueError("ожидание истекло")

        async def on_error(self, exc):
            log.append(f"handler.on_error:{exc}")

        dp = dispatcher(make("H", after_handle=after_handle, on_error=on_error))
        await feed(dp)
        await settle(dp)
        assert log[-1] == "handler.on_error:ожидание истекло"

    async def test_defer_failure_is_routed_like_handler_failure(self, telegram):
        async def handle(self):
            self.defer(boom)

        dp = dispatcher(make("H", handle=handle))
        await feed(dp)
        await settle(dp)
        assert log[-1] == "dispatcher.on_error:RuntimeError:отложенное упало"

    async def test_slow_after_handle_does_not_hold_the_update_slot(self, telegram):
        async def after_handle(self):
            await asyncio.sleep(0.4)

        dp = dispatcher(make("H", after_handle=after_handle), max_concurrent_updates=1)
        started = asyncio.get_running_loop().time()
        for _ in range(3):
            await dp.feed_update(
                bind(message_update("go"), dp.api)
            )  # ждал бы слот, будь он занят
        await dp._runner.drain()
        assert (
            asyncio.get_running_loop().time() - started < 0.3
        )  # три хендлера, а ожидания идут параллельно
        assert dp._background.active == 3
        await dp._background.drain(0.05)


class TestIsolationAndLimits:
    async def test_contextvar_of_middleware_is_not_visible(self, telegram):
        session: ContextVar[str] = ContextVar("session")
        seen = []

        class Db(Trace):
            async def pre_handle(self) -> bool:
                self.token = session.set("сессия")
                return True

            async def post_handle(self, exc=None):
                session.reset(self.token)

        async def check() -> None:
            seen.append(session.get("нет"))

        async def handle(self):
            seen.append(session.get("нет"))  # в хендлере она есть
            self.defer(check)

        dp = dispatcher(make("H", handle=handle), middlewares=(Db,))
        await feed(dp)
        await settle(dp)
        assert seen == ["сессия", "нет"]  # в отложенном чистый контекст

    async def test_limit_raises_in_handler(self, telegram):
        results = []

        async def handle(self):
            for _ in range(3):
                try:
                    self.defer(note, "x", delay=0.2)
                    results.append("ok")
                except DeferredLimitError:
                    results.append("limit")

        dp = dispatcher(make("H", handle=handle), max_deferred=2)
        dp._background.limit = 2
        await feed(dp)
        assert results == ["ok", "ok", "limit"]
        await dp._background.drain(0.05)

    async def test_after_handle_over_limit_goes_to_on_error(self, telegram):
        async def after_handle(self):
            await asyncio.sleep(0.3)

        async def on_error(self, exc):
            log.append(f"handler.on_error:{type(exc).__name__}")

        dp = dispatcher(make("H", after_handle=after_handle, on_error=on_error))
        dp._background.limit = 1
        await feed(dp)
        await feed(dp)  # второй after_handle: места нет
        assert log[-1] == "handler.on_error:DeferredLimitError"
        await dp._background.drain(0.05)

    async def test_tasks_are_referenced_until_done_then_released(self, telegram):
        async def handle(self):
            self.defer(note, "x", delay=0.1)

        dp = dispatcher(make("H", handle=handle))
        await feed(dp)
        assert dp._background.active == 1
        assert len(dp._background._items) == 1  # ссылка держится: GC не съест
        await settle(dp)
        assert dp._background.active == 0
        assert not dp._background._items


class TestShutdown:
    async def test_sleeping_timers_are_cancelled_and_running_awaited(self, telegram):
        async def handle(self):
            self.defer(note, "таймер на час", delay=3600)
            self.defer(note, "идущее", delay=0)

        async def after_handle(self):
            await asyncio.sleep(0.15)
            log.append("after доработал")

        dp = dispatcher(
            make("H", handle=handle, after_handle=after_handle), shutdown_timeout=2.0
        )
        await feed(dp)
        await asyncio.sleep(0.02)

        started = asyncio.get_running_loop().time()
        await dp._stop(started=False)
        assert asyncio.get_running_loop().time() - started < 1.0  # не ждал час
        assert "таймер на час" not in log  # спящий отменён
        assert "after доработал" in log  # идущий дождались

    async def test_running_over_timeout_is_cancelled(self, telegram):
        cancelled = []

        async def after_handle(self):
            try:
                await asyncio.sleep(30)
            except asyncio.CancelledError:
                cancelled.append(1)
                raise

        dp = dispatcher(make("H", after_handle=after_handle), shutdown_timeout=0.2)
        await feed(dp)
        await asyncio.sleep(0.02)
        await dp._stop(started=False)
        assert cancelled == [1]
