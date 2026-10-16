"""Фоновые периодические задачи: BaseTask, Every, Dispatcher.tasks."""

import asyncio

import pytest

from selfrot import BaseContext, BaseDispatcher, BaseMiddleware, BaseTask, Bot, Every
from selfrot.exceptions import DefinitionError

log: list[str] = []


@pytest.fixture(autouse=True)
def clean_log():
    log.clear()


class Trace(BaseMiddleware):
    async def pre_handle(self) -> bool:
        log.append(f"pre(background={self.ctx.is_background})")
        return True

    async def post_handle(self, exc=None):
        log.append(f"post({type(exc).__name__ if exc else None})")


class TestEvery:
    def test_rejects_non_positive_interval(self):
        class T(BaseTask):
            async def run(self): ...

        with pytest.raises(DefinitionError, match="interval"):
            Every(0, T)
        with pytest.raises(DefinitionError, match="interval"):
            Every(-5, T)

    def test_repr(self):
        class MarriageExpiry(BaseTask):
            async def run(self): ...

        assert repr(Every(30, MarriageExpiry)) == "Every(30, MarriageExpiry)"


class TestBaseTask:
    def test_cannot_instantiate_without_run(self):
        with pytest.raises(TypeError):
            BaseTask(ctx=None)  # type: ignore[abstract, arg-type]

    async def test_default_on_error_reraises(self):
        class T(BaseTask):
            async def run(self): ...

        task = T(ctx=None)  # type: ignore[arg-type]
        with pytest.raises(RuntimeError, match="боль"):
            await task.on_error(RuntimeError("боль"))


class TestRunTask:
    def dispatcher(self, task_cls, **extra) -> BaseDispatcher:
        class Root(BaseDispatcher[BaseContext]):
            bot = Bot
            context = BaseContext
            middlewares = (Trace,)
            tasks = (Every(1000, task_cls),)

        for name, value in extra.items():
            setattr(Root, name, value)

        return Root(token="1:T")

    async def test_public_and_does_not_need_the_task_to_be_registered_in_tasks(self):
        # Запрос с продакшена: один прогон для ручного вызова (админ-команда, тест
        # фоновой задачи) без ожидания интервала — и не обязательно той задачи,
        # которая вообще стоит в Dispatcher.tasks.
        class NotRegistered(BaseTask):
            async def run(self):
                log.append("ran")

        class Root(BaseDispatcher[BaseContext]):
            bot = Bot
            context = BaseContext
            # tasks вообще не задан — run_task не привязан к Every/tasks.

        dp = Root(token="1:T")
        await dp.run_task(NotRegistered)
        assert log == ["ran"]
        await dp.api.close_session()

    async def test_context_is_flagged_background_and_has_no_update_fields(self):
        seen = {}

        class Inspect(BaseTask):
            async def run(self):
                seen["is_background"] = self.ctx.is_background
                seen["chat"] = self.ctx.chat
                seen["user"] = self.ctx.user

        dp = self.dispatcher(Inspect)
        await dp.run_task(Inspect)
        assert seen == {"is_background": True, "chat": None, "user": None}
        await dp.api.close_session()

    async def test_middlewares_run_around_the_task(self):
        class Noop(BaseTask):
            async def run(self):
                log.append("run")

        dp = self.dispatcher(Noop)
        await dp.run_task(Noop)
        assert log == ["pre(background=True)", "run", "post(None)"]
        await dp.api.close_session()

    async def test_each_run_gets_a_fresh_context(self):
        # Ссылки на сами объекты, не id(): если первый ctx уже собран сборщиком
        # мусора до создания второго, id() может совпасть по чистой случайности
        # (это просто адрес памяти) — ссылка держит объект живым до сравнения.
        seen = []

        class Inspect(BaseTask):
            async def run(self):
                seen.append(self.ctx)

        dp = self.dispatcher(Inspect)
        await dp.run_task(Inspect)
        await dp.run_task(Inspect)
        assert seen[0] is not seen[1]
        await dp.api.close_session()

    async def test_task_handles_its_own_error(self):
        class HandlesItself(BaseTask):
            async def run(self):
                raise RuntimeError("упал")

            async def on_error(self, exc):
                log.append(f"task.on_error:{exc}")

        dp = self.dispatcher(HandlesItself)
        await dp.run_task(HandlesItself)
        assert log[-1] == "task.on_error:упал"
        assert "post(RuntimeError)" in log  # мидлвари видят ошибку, сессия откатится
        await dp.api.close_session()

    async def test_unhandled_error_goes_to_dispatcher_on_error(self):
        class Unhandled(BaseTask):
            async def run(self):
                raise RuntimeError("совсем упал")

        async def on_error(self, ctx, exc):
            log.append(f"dispatcher.on_error:{exc}")

        dp = self.dispatcher(Unhandled, on_error=on_error)
        await dp.run_task(Unhandled)
        assert log[-1] == "dispatcher.on_error:совсем упал"
        await dp.api.close_session()

    async def test_failing_dispatcher_on_error_does_not_crash(self):
        class Unhandled(BaseTask):
            async def run(self):
                raise RuntimeError("упал")

        async def on_error(self, ctx, exc):
            raise KeyError("и on_error упал")

        dp = self.dispatcher(Unhandled, on_error=on_error)
        await dp.run_task(Unhandled)  # не бросает наружу
        await dp.api.close_session()


class TestScheduling:
    async def test_runs_repeatedly_at_its_own_interval(self):
        class Tick(BaseTask):
            async def run(self):
                log.append("tick")

        class Root(BaseDispatcher[BaseContext]):
            bot = Bot
            context = BaseContext
            tasks = (Every(0.03, Tick),)

        dp = Root(token="1:T")
        dp._start_tasks()
        await asyncio.sleep(0.1)
        await dp._stop_tasks()
        assert 2 <= len(log) <= 4  # ~3 тика за 0.1с с шагом 0.03с, с запасом
        await dp.api.close_session()

    async def test_independent_intervals_for_several_tasks(self):
        class Fast(BaseTask):
            async def run(self):
                log.append("fast")

        class Slow(BaseTask):
            async def run(self):
                log.append("slow")

        class Root(BaseDispatcher[BaseContext]):
            bot = Bot
            context = BaseContext
            tasks = (Every(0.02, Fast), Every(0.2, Slow))

        dp = Root(token="1:T")
        dp._start_tasks()
        await asyncio.sleep(0.09)
        await dp._stop_tasks()
        assert log.count("fast") >= 2
        assert log.count("slow") == 0  # интервал ещё не подошёл
        await dp.api.close_session()

    async def test_stop_finishes_an_in_flight_tick_instead_of_cutting_it_off(self):
        class Slow(BaseTask):
            async def run(self):
                log.append("start")
                await asyncio.sleep(0.15)
                log.append("finish")

        class Root(BaseDispatcher[BaseContext]):
            bot = Bot
            context = BaseContext
            tasks = (Every(0.02, Slow),)

        dp = Root(token="1:T")
        dp._start_tasks()
        await asyncio.sleep(0.05)  # тик уже начался, но ещё не закончился
        await dp._stop_tasks()
        assert log == ["start", "finish"]  # ровно один, доработал до конца
        await dp.api.close_session()

    async def test_stop_while_sleeping_is_immediate(self):
        class Tick(BaseTask):
            async def run(self):
                log.append("tick")

        class Root(BaseDispatcher[BaseContext]):
            bot = Bot
            context = BaseContext
            tasks = (Every(10, Tick),)  # не успеет сработать за тест

        dp = Root(token="1:T")
        dp._start_tasks()
        started = asyncio.get_running_loop().time()
        await dp._stop_tasks()
        assert asyncio.get_running_loop().time() - started < 1.0
        assert log == []
        await dp.api.close_session()


class TestPollingIntegration:
    async def test_tasks_start_after_on_startup_and_stop_with_polling(
        self, telegram
    ):
        telegram.on("getUpdates", lambda _b: [])

        class Tick(BaseTask):
            async def run(self):
                log.append("tick")

        class Root(BaseDispatcher[BaseContext]):
            bot = Bot
            context = BaseContext
            tasks = (Every(0.02, Tick),)
            polling_timeout = 0

            async def on_startup(self):
                log.append("startup")

            async def on_shutdown(self):
                log.append("shutdown")

        dp = Root(token="1:T")
        task = asyncio.create_task(dp.polling())
        await asyncio.sleep(0.09)
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task

        assert log[0] == "startup"
        assert "tick" in log  # задача реально стартовала вместе с поллингом
        assert log[-1] == "shutdown"
