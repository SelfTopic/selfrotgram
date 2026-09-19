import asyncio
from dataclasses import dataclass
from typing import Any, ClassVar

import pytest
from aiohttp import web

from selfrot import Bot, BotDefaults
from selfrot.client.telegram import TELEGRAM_API
from selfrot.exceptions import (
    ConfigError,
    TelegramNetworkError,
    TelegramRetryAfter,
    TelegramServerError,
    TelegramTimeout,
)
from selfrot.methods import SendMessage
from selfrot.methods.base import TelegramMethod
from selfrot.types import (
    InlineQueryResultArticle,
    InputMediaPhoto,
    InputTextMessageContent,
    LinkPreviewOptions,
)

from .conftest import TOKEN, FakeTelegram, message_result


def method(name: str):
    @dataclass
    class Raw(TelegramMethod[Any]):
        __api_method__: ClassVar[str] = name
        __returning__: ClassVar[Any] = dict

    return Raw()


class FastBot(Bot):
    request_timeout = 1.0
    connect_timeout = 1.0
    flood_max_wait = 30.0


@pytest.fixture
async def fast(telegram) -> Bot:
    api = FastBot(TOKEN)
    yield api
    await api.close_session()


class TestErrors:
    async def test_502_html_becomes_server_error(self, telegram, fast):
        telegram.on(
            "boom",
            lambda _b: web.Response(
                text="<html>502 Bad Gateway</html>",
                status=502,
                content_type="text/html",
            ),
        )
        with pytest.raises(TelegramServerError):
            await fast.call(method("boom"))

    async def test_slow_answer_is_timeout(self, telegram, fast):
        # Медленный сервер: подменяем адрес API на него.
        app = web.Application()

        async def hang(request):
            await asyncio.sleep(3)
            return web.json_response({"ok": True, "result": {}})

        app.router.add_route("*", "/bot{token}/{method}", hang)
        runner = web.AppRunner(app, access_log=None)
        await runner.setup()
        site = web.TCPSite(runner, "127.0.0.1", 0)
        await site.start()
        port = site._server.sockets[0].getsockname()[1]
        TELEGRAM_API.url = f"http://127.0.0.1:{port}/bot{{token}}/{{method}}"
        try:
            with pytest.raises(TelegramTimeout, match="1 с"):
                await fast.call(method("slow"))
        finally:
            await runner.cleanup()

    async def test_closed_port_is_network_error_without_token(self, monkeypatch, fast):
        monkeypatch.setattr(
            TELEGRAM_API, "url", "http://127.0.0.1:1/bot{token}/{method}"
        )
        with pytest.raises(TelegramNetworkError) as info:
            await fast.call(method("getMe"))

        assert not isinstance(info.value, TelegramTimeout)
        assert TOKEN not in str(
            info.value
        )  # aiohttp кладёт URL с токеном в свои ошибки
        assert info.value.__cause__ is None

    async def test_proxy_address_is_not_leaked(self, monkeypatch):
        class Proxied(FastBot):
            proxy = "http://user:secret@127.0.0.1:1"

        api = Proxied(TOKEN)
        try:
            with pytest.raises(TelegramNetworkError) as info:
                await api.call(method("getMe"))
            assert "secret" not in str(info.value)
        finally:
            await api.close_session()


class TestFloodControl:
    def flood(self, telegram: FakeTelegram, times: int, retry_after: int = 1):
        state = {"n": 0}

        def handler(_body):
            state["n"] += 1
            if state["n"] <= times:
                return web.json_response(
                    {
                        "ok": False,
                        "error_code": 429,
                        "description": "Too Many Requests",
                        "parameters": {"retry_after": retry_after},
                    },
                    status=429,
                )
            return {"id": 1}

        telegram.on("flood", handler)
        return state

    async def test_waits_and_retries_429(self, telegram, fast):
        state = self.flood(telegram, times=2)
        started = asyncio.get_running_loop().time()
        await fast.call(method("flood"))
        assert state["n"] == 3
        assert asyncio.get_running_loop().time() - started >= 1.9

    async def test_long_wait_is_raised_not_slept(self, telegram, fast):
        self.flood(telegram, times=5, retry_after=100)
        with pytest.raises(TelegramRetryAfter) as info:
            await fast.call(method("flood"))
        assert info.value.retry_after == 100

    async def test_retries_can_be_disabled(self, telegram):
        class NoRetry(FastBot):
            flood_retries = 0

        state = self.flood(telegram, times=5)
        api = NoRetry(TOKEN)
        try:
            with pytest.raises(TelegramRetryAfter):
                await api.call(method("flood"))
            assert state["n"] == 1
        finally:
            await api.close_session()


class TestDefaults:
    NO_PREVIEW = LinkPreviewOptions(is_disabled=True)

    def bot_with(self, **defaults) -> Bot:
        class Configured(Bot):
            pass

        Configured.defaults = BotDefaults(**defaults)
        return Configured(TOKEN)

    async def test_link_preview_default_is_applied(self, telegram):
        api = self.bot_with(link_preview_options=self.NO_PREVIEW)
        await api.send_message(1, "текст")
        assert telegram.sent[-1] == {
            "chat_id": 1,
            "text": "текст",
            "link_preview_options": {"is_disabled": True},
        }
        await api.close_session()

    async def test_explicit_value_beats_default(self, telegram):
        api = self.bot_with(
            parse_mode="HTML",
            disable_notification=True,
            link_preview_options=self.NO_PREVIEW,
        )
        await api.send_message(
            1,
            "x",
            parse_mode="MarkdownV2",
            disable_notification=False,
            link_preview_options=LinkPreviewOptions(is_disabled=False),
        )
        body = telegram.sent[-1]
        assert body["parse_mode"] == "MarkdownV2"
        assert body["disable_notification"] is False
        assert body["link_preview_options"] == {"is_disabled": False}
        await api.close_session()

    async def test_applies_to_nested_objects(self, telegram):
        api = self.bot_with(
            parse_mode="HTML",
            link_preview_options=self.NO_PREVIEW,
            show_caption_above_media=True,
        )
        telegram.on("sendMediaGroup", [message_result()])
        await api.send_media_group(
            1,
            media=[
                InputMediaPhoto(media="a", caption="1"),
                InputMediaPhoto(media="b", parse_mode="Markdown"),
            ],
        )
        media = telegram.last()[1]["media"]
        assert (media[0]["parse_mode"], media[1]["parse_mode"]) == ("HTML", "Markdown")
        assert media[0]["show_caption_above_media"] is True

        await api.answer_inline_query(
            "q",
            results=[
                InlineQueryResultArticle(
                    id="1",
                    title="t",
                    input_message_content=InputTextMessageContent(message_text="hi"),
                )
            ],
        )
        content = telegram.last()[1]["results"][0]["input_message_content"]
        assert content["parse_mode"] == "HTML"
        assert content["link_preview_options"] == {"is_disabled": True}
        await api.close_session()

    async def test_methods_without_such_fields_untouched_and_original_not_mutated(
        self, telegram
    ):
        api = self.bot_with(parse_mode="HTML")
        await api.get_me()
        assert telegram.last() == ("getMe", {})
        original = SendMessage(chat_id=1, text="t")
        assert api.defaults.apply(original).parse_mode == "HTML"
        assert original.parse_mode is None
        await api.close_session()

    async def test_no_defaults_no_changes(self, telegram, bot):
        await bot.send_message(1, "x")
        assert telegram.sent[-1] == {"chat_id": 1, "text": "x"}


class TestBotConstruction:
    @pytest.mark.parametrize("token", ["YOUR_BOT_TOKEN", "", "abc", "123:"])
    def test_bad_tokens(self, token):
        with pytest.raises(ConfigError):
            Bot(token)

    def test_token_argument_writes_nothing_to_disk(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        Bot("123456:ABC-def")
        assert list(tmp_path.iterdir()) == []

    def test_without_token_reads_config_file(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        (tmp_path / "bot_cfg.cfg").write_text("[DEFAULT]\nbot_token = 555:FROM-FILE\n")
        assert Bot().token == "555:FROM-FILE"

    def test_without_token_and_file_creates_placeholder_and_fails(
        self, tmp_path, monkeypatch
    ):
        monkeypatch.chdir(tmp_path)
        with pytest.raises(ConfigError):
            Bot()
        assert (tmp_path / "bot_cfg.cfg").exists()
