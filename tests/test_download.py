"""Скачивание файлов: bot.download_file, bot.download, ctx.download."""

import asyncio
from collections.abc import AsyncIterator
from pathlib import Path

import pytest
from aiohttp import web

from selfrot import BaseContext, Bot
from selfrot.client.telegram import TELEGRAM_FILE_API
from selfrot.exceptions import (
    ContextError,
    FileNotAvailableError,
    TelegramAPIError,
    TelegramNetworkError,
    TelegramTimeout,
)

from .conftest import (
    REPLY_SAMPLES,
    TOKEN,
    FakeTelegram,
    bind,
    callback_update,
    message_update,
    reply_update,
)


class FastBot(Bot):
    request_timeout = 1.0
    connect_timeout = 1.0


@pytest.fixture
async def fast(telegram: FakeTelegram) -> AsyncIterator[Bot]:
    api = FastBot(TOKEN)
    yield api
    await api.close_session()


def ctx(raw: dict, api: Bot) -> BaseContext:
    return BaseContext(bind(raw, api), api)


class TestBotDownloadFile:
    """Транспорт: bot.download_file(file_path) — сырые байты по известному пути."""

    async def test_downloads_bytes(self, telegram: FakeTelegram, fast: Bot):
        telegram.set_file("photos/1.jpg", b"\x89PNG-content")
        assert await fast.download_file("photos/1.jpg") == b"\x89PNG-content"
        assert telegram.downloads == ["photos/1.jpg"]

    async def test_missing_file_is_api_error(self, telegram: FakeTelegram, fast: Bot):
        with pytest.raises(TelegramAPIError) as info:
            await fast.download_file("no/such/path")

        assert info.value.error_code == 404
        assert info.value.method == "downloadFile"

    async def test_slow_server_is_timeout(self, fast: Bot):
        app = web.Application()

        async def hang(request: web.Request) -> web.Response:
            await asyncio.sleep(3)
            return web.Response(body=b"x")

        app.router.add_route("*", "/file/bot{token}/{file_path:.*}", hang)
        runner = web.AppRunner(app, access_log=None)
        await runner.setup()
        site = web.TCPSite(runner, "127.0.0.1", 0)
        await site.start()
        port = site._server.sockets[0].getsockname()[1]  # type: ignore[union-attr]
        TELEGRAM_FILE_API.url = f"http://127.0.0.1:{port}/file/bot{{token}}/{{file_path}}"
        try:
            with pytest.raises(TelegramTimeout, match="1 с"):
                await fast.download_file("slow.jpg")
        finally:
            await runner.cleanup()

    async def test_closed_port_is_network_error_without_token(
        self, monkeypatch: pytest.MonkeyPatch, fast: Bot
    ):
        monkeypatch.setattr(
            TELEGRAM_FILE_API, "url", "http://127.0.0.1:1/file/bot{token}/{file_path}"
        )
        with pytest.raises(TelegramNetworkError) as info:
            await fast.download_file("a.jpg")

        assert not isinstance(info.value, TelegramTimeout)
        assert TOKEN not in str(info.value)

    async def test_proxy_address_is_not_leaked(self, telegram: FakeTelegram):
        class Proxied(FastBot):
            proxy = "http://user:secret@127.0.0.1:1"

        api = Proxied(TOKEN)
        try:
            with pytest.raises(TelegramNetworkError) as info:
                await api.download_file("a.jpg")
            assert "secret" not in str(info.value)
        finally:
            await api.close_session()


class TestBotDownload:
    """bot.download(file_id): get_file + download_file в одном вызове."""

    async def test_downloads_by_file_id(self, telegram: FakeTelegram, fast: Bot):
        telegram.on(
            "getFile",
            {"file_id": "F1", "file_unique_id": "U1", "file_path": "documents/f1.pdf"},
        )
        telegram.set_file("documents/f1.pdf", b"pdf-bytes")

        assert await fast.download("F1") == b"pdf-bytes"
        assert telegram.methods() == ["getFile"]
        assert telegram.calls[0][1] == {"file_id": "F1"}

    async def test_missing_file_path_is_our_own_error(
        self, telegram: FakeTelegram, fast: Bot
    ):
        telegram.on("getFile", {"file_id": "F1", "file_unique_id": "U1"})  # без file_path
        with pytest.raises(FileNotAvailableError, match="F1"):
            await fast.download("F1")

        assert telegram.downloads == []  # до скачивания не дошло


class TestContextDownload:
    """ctx.download(destination): находит файл в апдейте сам, пишет на диск."""

    @pytest.mark.parametrize(
        "attr",
        ["animation", "audio", "document", "sticker", "video", "video_note", "voice"],
    )
    async def test_downloads_the_field_that_is_filled(
        self, telegram: FakeTelegram, fast: Bot, tmp_path: Path, attr: str
    ):
        telegram.on(
            "getFile",
            {"file_id": "F", "file_unique_id": "U", "file_path": "f.bin"},
        )
        telegram.set_file("f.bin", b"content")

        update = message_update(None, **REPLY_SAMPLES[attr])
        c = ctx(update, fast)

        out = tmp_path / "saved.bin"
        result = await c.download(out)

        assert result == out
        assert out.read_bytes() == b"content"
        assert telegram.calls[0] == ("getFile", {"file_id": "a"})  # id из REPLY_SAMPLES

    async def test_photo_picks_the_biggest_size(
        self, telegram: FakeTelegram, fast: Bot, tmp_path: Path
    ):
        small = {"file_id": "small", "file_unique_id": "u1", "width": 10, "height": 10}
        big = {"file_id": "big", "file_unique_id": "u2", "width": 200, "height": 100}

        def any_file(body: dict) -> dict:
            return {
                "file_id": body["file_id"],
                "file_unique_id": "u",
                "file_path": f"{body['file_id']}.jpg",
            }

        telegram.on("getFile", any_file)
        telegram.set_file("big.jpg", b"the-big-one")

        update = message_update(None, photo=[small, big])
        c = ctx(update, fast)

        out = await c.download(tmp_path / "photo.jpg")
        assert out.read_bytes() == b"the-big-one"
        assert telegram.calls[0][1] == {"file_id": "big"}

    async def test_missing_suffix_is_completed_from_telegrams_file_path(
        self, telegram: FakeTelegram, fast: Bot, tmp_path: Path
    ):
        telegram.on(
            "getFile",
            {"file_id": "F", "file_unique_id": "U", "file_path": "photos/x.jpg"},
        )
        telegram.set_file("photos/x.jpg", b"content")

        update = message_update(None, **REPLY_SAMPLES["document"])
        c = ctx(update, fast)

        out = await c.download(tmp_path / "1")  # без расширения
        assert out == tmp_path / "1.jpg"  # добавлено из настоящего file_path
        assert out.read_bytes() == b"content"

    @pytest.mark.parametrize("attr", ["animation", "audio", "document", "video"])
    async def test_suffix_prefers_the_original_filename_over_file_path(
        self, telegram: FakeTelegram, fast: Bot, tmp_path: Path, attr: str
    ):
        # file_path нарочно с другим расширением: показывает, что победил file_name.
        telegram.on(
            "getFile", {"file_id": "F", "file_unique_id": "U", "file_path": "x.bin"}
        )
        telegram.set_file("x.bin", b"content")

        media = {**REPLY_SAMPLES[attr][attr], "file_name": "report.txt"}
        update = message_update(None, **{attr: media})
        c = ctx(update, fast)

        out = await c.download(tmp_path / "1")
        assert out == tmp_path / "1.txt"

    @pytest.mark.parametrize("attr", ["photo", "sticker", "video_note", "voice"])
    async def test_types_without_original_filename_still_fall_back_to_file_path(
        self, telegram: FakeTelegram, fast: Bot, tmp_path: Path, attr: str
    ):
        # У этих типов file_name физически нет: подставляется расширение из file_path.
        telegram.on(
            "getFile", {"file_id": "F", "file_unique_id": "U", "file_path": "x.bin"}
        )
        telegram.set_file("x.bin", b"content")

        update = message_update(None, **REPLY_SAMPLES[attr])
        c = ctx(update, fast)

        out = await c.download(tmp_path / "1")
        assert out == tmp_path / "1.bin"

    async def test_given_suffix_is_not_overridden(
        self, telegram: FakeTelegram, fast: Bot, tmp_path: Path
    ):
        telegram.on(
            "getFile",
            {"file_id": "F", "file_unique_id": "U", "file_path": "photos/x.jpg"},
        )
        telegram.set_file("photos/x.jpg", b"content")

        update = message_update(None, **REPLY_SAMPLES["document"])
        c = ctx(update, fast)

        out = await c.download(tmp_path / "1.bin")  # своё расширение, пусть и «неверное»
        assert out == tmp_path / "1.bin"

    async def test_overwrite_true_replaces_silently_by_default(
        self, telegram: FakeTelegram, fast: Bot, tmp_path: Path
    ):
        telegram.on(
            "getFile", {"file_id": "F", "file_unique_id": "U", "file_path": "d.bin"}
        )
        out = tmp_path / "d.bin"
        out.write_bytes(b"old")

        telegram.set_file("d.bin", b"new")
        update = message_update(None, **REPLY_SAMPLES["document"])
        result = await ctx(update, fast).download(out)  # overwrite не задан, по умолчанию True

        assert result == out
        assert out.read_bytes() == b"new"

    async def test_overwrite_false_numbers_instead_of_replacing(
        self, telegram: FakeTelegram, fast: Bot, tmp_path: Path
    ):
        telegram.on(
            "getFile", {"file_id": "F", "file_unique_id": "U", "file_path": "d.bin"}
        )
        telegram.set_file("d.bin", b"content")
        update = message_update(None, **REPLY_SAMPLES["document"])
        dest = tmp_path / "d.bin"
        dest.write_bytes(b"already here")  # чужой файл, трогать нельзя

        first = await ctx(update, fast).download(dest, overwrite=False)
        second = await ctx(update, fast).download(dest, overwrite=False)
        third = await ctx(update, fast).download(dest, overwrite=False)

        assert first == tmp_path / "d (1).bin"
        assert second == tmp_path / "d (2).bin"
        assert third == tmp_path / "d (3).bin"
        assert dest.read_bytes() == b"already here"  # не тронут
        for path in (first, second, third):
            assert path.read_bytes() == b"content"

    async def test_no_media_raises_context_error(self, fast: Bot):
        c = ctx(message_update("просто текст"), fast)
        with pytest.raises(ContextError, match="нет файла"):
            await c.download("out.bin")

    async def test_no_media_at_all_including_the_reply_raises(self, fast: Bot):
        # /save в ответ на обычный текст: медиа нет ни у команды, ни у того, что процитировали.
        c = ctx(reply_update("/save", {"text": "просто текст"}), fast)
        with pytest.raises(ContextError, match="нет файла"):
            await c.download("out.bin")

    async def test_falls_back_to_the_replied_message(
        self, telegram: FakeTelegram, fast: Bot, tmp_path: Path
    ):
        # /save текстом в ответ на чьё-то фото: у самой команды медиа нет, у ответа — есть.
        telegram.on(
            "getFile", {"file_id": "F", "file_unique_id": "U", "file_path": "p.jpg"}
        )
        telegram.set_file("p.jpg", b"reply-bytes")

        c = ctx(reply_update("/save", REPLY_SAMPLES["photo"]), fast)
        out = await c.download(tmp_path / "p.jpg")

        assert out.read_bytes() == b"reply-bytes"
        assert telegram.calls[0][1] == {"file_id": "a"}  # id из REPLY_SAMPLES

    async def test_own_message_wins_over_the_reply(
        self, telegram: FakeTelegram, fast: Bot, tmp_path: Path
    ):
        # И у команды, и у того, на что она отвечает, есть медиа: берём то, что прислали сейчас.
        telegram.on(
            "getFile", {"file_id": "F", "file_unique_id": "U", "file_path": "own.bin"}
        )
        telegram.set_file("own.bin", b"own-bytes")

        raw = reply_update(
            "/save",
            REPLY_SAMPLES["photo"],
            document={"file_id": "own", "file_unique_id": "u"},
        )
        c = ctx(raw, fast)
        await c.download(tmp_path / "out.bin")

        assert telegram.calls[0][1] == {"file_id": "own"}  # не "a" (из reply)

    async def test_works_from_callback_message(
        self, telegram: FakeTelegram, fast: Bot, tmp_path: Path
    ):
        telegram.on(
            "getFile",
            {"file_id": "F", "file_unique_id": "U", "file_path": "voice.ogg"},
        )
        telegram.set_file("voice.ogg", b"voice-bytes")

        raw = callback_update("x")
        raw["callback_query"]["message"].update(REPLY_SAMPLES["voice"])
        c = ctx(raw, fast)

        out = await c.download(tmp_path / "voice.ogg")
        assert out.read_bytes() == b"voice-bytes"

    async def test_writes_asynchronously_not_blocking(
        self, telegram: FakeTelegram, fast: Bot, tmp_path: Path
    ):
        # asyncio.to_thread для записи: просто проверяем, что путь реально появился на диске.
        telegram.on(
            "getFile",
            {"file_id": "F", "file_unique_id": "U", "file_path": "d.bin"},
        )
        telegram.set_file("d.bin", b"12345")
        c = ctx(message_update(None, **REPLY_SAMPLES["document"]), fast)

        out = tmp_path / "nested" / "d.bin"
        assert not out.parent.exists()
        with pytest.raises(FileNotFoundError):
            await c.download(out)  # директории сами не создаются — явное поведение
