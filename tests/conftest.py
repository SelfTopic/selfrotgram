"""
Общие средства тестов: фейковый Telegram (настоящий HTTP-сервер на localhost) и
сборщики апдейтов. Ничего не ходит в сеть: адрес API подменяется на локальный.
"""

import inspect
import json
import sys
from collections.abc import AsyncIterator, Callable
from pathlib import Path
from typing import Any

import pytest
from aiohttp import web
from pydantic import TypeAdapter

from selfrot import Bot
from selfrot.client.telegram import TELEGRAM_API, TELEGRAM_FILE_API
from selfrot.types import Update

TOKEN = "123456:TEST-token"


def message_result(text: str = "x", message_id: int = 100, chat_id: int = 1) -> dict:
    return {
        "message_id": message_id,
        "date": 5,
        "chat": {"id": chat_id, "type": "private"},
        "text": text,
    }


ME = {"id": 123456, "is_bot": True, "first_name": "Bot", "username": "test_bot"}
# Что Telegram возвращает по умолчанию; тест может подменить через telegram.on(...).
DEFAULT_RESULTS: dict[str, Any] = {
    "getMe": ME,
    "getUpdates": [],
    "deleteMessage": True,
    "pinChatMessage": True,
    "answerCallbackQuery": True,
    "answerInlineQuery": True,
    "setWebhook": True,
    "deleteWebhook": True,
}


class FakeTelegram:
    """Записывает все вызовы Bot API и отвечает заготовками."""

    def __init__(self) -> None:
        self.calls: list[tuple[str, dict[str, Any]]] = []
        self._handlers: dict[
            str, Callable[[dict[str, Any]], web.StreamResponse | Any]
        ] = {}
        self.url = ""
        # file_path -> содержимое; не заведён — 404 (как у настоящего Telegram на чужой путь).
        self._files: dict[str, bytes] = {}
        self.downloads: list[str] = []  # file_path каждого запроса на скачивание

    def on(self, method: str, result: Any) -> None:
        """result — готовый ответ или функция (тело) -> ответ / web.Response (можно async)."""
        self._handlers[method] = (
            result if callable(result) else (lambda _b, r=result: r)
        )

    def set_file(self, file_path: str, content: bytes) -> None:
        """Что отдавать на скачивание file_path (см. TELEGRAM_FILE_API)."""
        self._files[file_path] = content

    @property
    def sent(self) -> list[dict[str, Any]]:
        """Тела всех sendMessage."""
        return [body for method, body in self.calls if method == "sendMessage"]

    def methods(self) -> list[str]:
        return [method for method, _ in self.calls]

    def last(self) -> tuple[str, dict[str, Any]]:
        return self.calls[-1]

    def clear(self) -> None:
        self.calls.clear()

    async def _handle(self, request: web.Request) -> web.StreamResponse:
        method = request.match_info["method"]
        body = json.loads(await request.text() or "{}")
        self.calls.append((method, body))

        handler = self._handlers.get(method)
        result = (
            handler(body) if handler else DEFAULT_RESULTS.get(method, message_result())
        )
        if inspect.isawaitable(result):
            result = await result
        if isinstance(result, web.StreamResponse):
            return result

        return web.json_response({"ok": True, "result": result})

    async def _handle_file(self, request: web.Request) -> web.StreamResponse:
        file_path = request.match_info["file_path"]
        self.downloads.append(file_path)
        content = self._files.get(file_path)
        if content is None:
            return web.Response(status=404, text="Not Found")

        return web.Response(body=content)


@pytest.fixture
async def telegram(monkeypatch: pytest.MonkeyPatch) -> AsyncIterator[FakeTelegram]:
    fake = FakeTelegram()
    app = web.Application()
    app.router.add_route("*", "/bot{token}/{method}", fake._handle)
    app.router.add_route("*", "/file/bot{token}/{file_path:.*}", fake._handle_file)
    runner = web.AppRunner(app, access_log=None)
    await runner.setup()
    site = web.TCPSite(runner, "127.0.0.1", 0)
    await site.start()

    port = site._server.sockets[0].getsockname()[1]  # type: ignore[union-attr]
    fake.url = f"http://127.0.0.1:{port}"
    monkeypatch.setattr(TELEGRAM_API, "url", f"{fake.url}/bot{{token}}/{{method}}")
    monkeypatch.setattr(
        TELEGRAM_FILE_API, "url", f"{fake.url}/file/bot{{token}}/{{file_path}}"
    )

    yield fake
    await runner.cleanup()


@pytest.fixture
async def bot(telegram: FakeTelegram) -> AsyncIterator[Bot]:
    api = Bot(TOKEN)
    yield api
    await api.close_session()


USER = {"id": 7, "is_bot": False, "first_name": "Вася"}


def chat_dict(chat_id: int) -> dict[str, Any]:
    if chat_id < 0:
        return {"id": chat_id, "type": "supergroup", "title": "группа"}
    return {"id": chat_id, "type": "private", "first_name": "Вася"}


def message_update(
    text: str | None = "x", uid: int = 7, chat: int | None = None, **extra: Any
) -> dict[str, Any]:
    message: dict[str, Any] = {
        "message_id": 1,
        "date": 5,
        "chat": chat_dict(chat if chat is not None else uid),
        "from": {**USER, "id": uid},
        **extra,
    }
    if text is not None:
        message["text"] = text

    return {"update_id": 1, "message": message}


FILE = {"file_id": "a", "file_unique_id": "b"}
ENTITIES = [{"type": "bold", "offset": 0, "length": 1}]

# Как выглядит сообщение, на которое ответили, для каждого готового условия над ответом
# (те, что перечислены в REPLY_ATTRS генератора).
REPLY_SAMPLES: dict[str, dict[str, Any]] = {
    "user": {"from": {"id": 99, "is_bot": False, "first_name": "Петя"}},
    "text": {"text": "привет"},
    "entities": {"entities": ENTITIES},
    "caption": {"caption": "подпись"},
    "caption_entities": {"caption_entities": ENTITIES},
    "photo": {"photo": [{**FILE, "width": 1, "height": 1}]},
    "animation": {"animation": {**FILE, "width": 1, "height": 1, "duration": 1}},
    "audio": {"audio": {**FILE, "duration": 1}},
    "document": {"document": FILE},
    "sticker": {
        "sticker": {
            **FILE,
            "type": "regular",
            "width": 1,
            "height": 1,
            "is_animated": False,
            "is_video": False,
        }
    },
    "video": {"video": {**FILE, "width": 1, "height": 1, "duration": 1}},
    "video_note": {"video_note": {**FILE, "length": 1, "duration": 1}},
    "voice": {"voice": {**FILE, "duration": 1}},
}


def reply_update(text: str, reply: dict[str, Any] | None, **extra: Any) -> dict[str, Any]:
    """Сообщение text, ответом на другое (поля которого reply); reply=None: не ответ."""
    if reply is not None:
        extra["reply_to_message"] = {
            "message_id": 5,
            "date": 1,
            "chat": {"id": 7, "type": "private", "first_name": "В"},
            **reply,
        }

    return message_update(text, **extra)


def callback_update(
    data: str | None, uid: int = 7, chat: int = 7, message_id: int = 44
) -> dict[str, Any]:
    return {
        "update_id": 1,
        "callback_query": {
            "id": "cq1",
            "from": {**USER, "id": uid},
            "chat_instance": "ci",
            **({"data": data} if data is not None else {}),
            "message": {
                "message_id": message_id,
                "date": 5,
                "chat": chat_dict(chat),
                "text": "кнопки",
            },
        },
    }


def bind(raw: dict[str, Any], api: Bot | None) -> Update:
    """Разобрать апдейт так, как это делает Bot/вебхук: объекты знают своего бота."""
    return TypeAdapter(Update).validate_python(raw, context={"bot": api})


@pytest.fixture
def project(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Пустая папка проекта; импорты сгенерированного кода не оседают между тестами."""
    monkeypatch.chdir(tmp_path)
    monkeypatch.syspath_prepend(str(tmp_path))
    before = set(sys.modules)
    yield tmp_path
    for name in set(sys.modules) - before:
        if name.split(".")[0] in {"src", "app", "mybot"}:
            del sys.modules[name]
