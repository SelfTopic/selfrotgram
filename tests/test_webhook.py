import asyncio
import socket

import aiohttp
import pytest

from selfrot import BaseContext, BaseDispatcher, Bot, MessageHandler
from selfrot.exceptions import ConfigError
from selfrot.filter import Text
from selfrot.types import TextMessage

from .conftest import FakeTelegram, message_update

SECRET = "s3cret_-Token"
events: list[str] = []


def free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


class Work(MessageHandler[BaseContext[TextMessage]]):
    query = Text("hi") | Text("slow")

    async def handle(self) -> None:
        text = self.ctx.message.text
        events.append(f"start:{text}")
        await asyncio.sleep(0.5 if text == "slow" else 0)
        await self.ctx.message.answer("привет из вебхука")
        events.append(f"end:{text}")


class Root(BaseDispatcher[BaseContext]):
    bot = Bot
    context = BaseContext
    handlers = (Work,)
    max_concurrent_updates = 2
    shutdown_timeout = 3.0

    async def on_startup(self):
        events.append("on_startup")

    async def on_shutdown(self):
        events.append("on_shutdown")


@pytest.fixture
async def server(telegram: FakeTelegram):
    events.clear()
    port = free_port()
    dp = Root(token="123456:TEST-token")

    async def listening_at_set_webhook(_body):
        try:
            async with (
                aiohttp.ClientSession() as s,
                s.post(f"http://127.0.0.1:{port}/hook", data="{}"),
            ):
                events.append("setWebhook(сервер слушает)")
        except aiohttp.ClientConnectionError:
            events.append("setWebhook(сервер НЕ слушает)")
        return True

    telegram.on("setWebhook", listening_at_set_webhook)
    task = asyncio.create_task(
        dp.webhook(
            url="https://example.org/hook",
            secret_token=SECRET,
            port=port,
            drop_pending_updates=True,
            max_connections=5,
        )
    )
    for _ in range(100):
        if "setWebhook" in telegram.methods():
            break
        await asyncio.sleep(0.05)

    yield dp, port, telegram

    if not task.done():
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task


async def post(
    port: int,
    data=None,
    secret: str | None = SECRET,
    path: str = "/hook",
    raw: str | None = None,
    method: str = "POST",
) -> int:
    headers = {"X-Telegram-Bot-Api-Secret-Token": secret} if secret is not None else {}
    url = f"http://127.0.0.1:{port}{path}"
    async with (
        aiohttp.ClientSession() as session,
        session.request(method, url, json=data, data=raw, headers=headers) as response,
    ):
        return response.status


def upd(update_id: int, text: str, chat: int = 7) -> dict:
    return message_update(text, chat=chat) | {"update_id": update_id}


class TestWebhook:
    async def test_startup_order_and_set_webhook_payload(self, server):
        _, _, telegram = server
        assert events[:2] == [
            "on_startup",
            "setWebhook(сервер слушает)",
        ]  # сервер поднят до setWebhook
        body = dict(telegram.calls)["setWebhook"]
        assert body == {
            "url": "https://example.org/hook",
            "secret_token": SECRET,
            "allowed_updates": ["message"],  # считается из дерева хендлеров
            "drop_pending_updates": True,
            "max_connections": 5,
        }

    @pytest.mark.parametrize(
        ("kwargs", "status"),
        [
            ({"secret": None}, 403),
            ({"secret": "wrong"}, 403),
            ({"secret": "секрет"}, 403),  # не-ASCII не должен давать 500
            ({"raw": "{oops"}, 400),
            ({"data": {"message": {}}}, 400),  # нет update_id
            ({"path": "/other"}, 404),
            ({"method": "GET"}, 405),
        ],
    )
    async def test_rejections(self, server, kwargs, status):
        _, port, _ = server
        if "raw" not in kwargs:
            kwargs.setdefault("data", upd(1, "hi"))
        assert await post(port, **kwargs) == status

    async def test_valid_update_is_answered_and_handled(self, server):
        _, port, telegram = server
        assert await post(port, upd(10, "hi")) == 200
        await asyncio.sleep(0.2)
        assert (
            telegram.sent[-1]["text"] == "привет из вебхука"
        )  # message.answer работает без ctx

    async def test_duplicate_update_id_is_dropped(self, server):
        _, port, telegram = server
        await post(port, upd(10, "hi"))
        await asyncio.sleep(0.2)
        telegram.clear()
        assert await post(port, upd(10, "hi")) == 200
        await asyncio.sleep(0.2)
        assert telegram.sent == []

    async def test_overload_returns_503_and_retry_is_accepted(self, server):
        _, port, telegram = server
        started = asyncio.get_running_loop().time()
        statuses = [
            await post(port, upd(21, "slow", chat=1)),
            await post(port, upd(22, "slow", chat=2)),
            await post(port, upd(23, "slow", chat=3)),
        ]
        assert statuses == [200, 200, 503]
        assert (
            asyncio.get_running_loop().time() - started < 0.4
        )  # отвечает сразу, а не после обработки

        await asyncio.sleep(0.7)
        telegram.clear()
        assert (
            await post(port, upd(23, "hi", chat=3)) == 200
        )  # 503 не запомнен как принятый
        await asyncio.sleep(0.2)
        assert telegram.sent

    async def test_shutdown_waits_for_handlers(self, server):
        dp, port, _ = server
        events.clear()
        await post(port, upd(31, "slow"))
        await asyncio.sleep(0.1)
        for task in asyncio.all_tasks():
            if task.get_coro().__qualname__.endswith("webhook"):
                task.cancel()
                with pytest.raises(asyncio.CancelledError):
                    await task
        assert events == ["start:slow", "end:slow", "on_shutdown"]
        assert dp.api.session.session is None

    @pytest.mark.parametrize("secret", ["", "с пробелом", "a b", "x" * 257])
    async def test_bad_secret_token_is_config_error(self, secret):
        with pytest.raises(ConfigError):
            await Root(token="1:T").webhook(url="https://x/y", secret_token=secret)
