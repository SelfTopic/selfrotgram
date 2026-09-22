"""Примеры не должны протухать: каждый импортируется и собирается в диспетчер."""

import importlib

import pytest

from selfrot import BaseDispatcher

# (модуль, класс диспетчера, нужный сторонний пакет)
EXAMPLES = [  # у каждого есть хендлеры
    ("examples.echo_bot", "Dispatcher", None),
    ("examples.filtered_bot", "Dispatcher", None),
    ("examples.deps_bot", "Dispatcher", None),
    ("examples.errors_bot", "Dispatcher", None),
    ("examples.keyboards_bot", "Dispatcher", None),
    ("examples.chat_members", "Dispatcher", None),
    ("examples.fsm_bot", "Dispatcher", None),
    ("examples.data_parsed_bot", "Dispatcher", None),
    ("examples.reply_bot", "Dispatcher", None),
    ("examples.download_bot", "Dispatcher", None),
    ("examples.deferred_bot", "Dispatcher", None),
    ("examples.webhook_bot", "Dispatcher", None),
    ("examples.db_bot", "Dispatcher", "sqlalchemy"),
    ("examples.bot_command.dispatcher", "AppDispatcher", "sqlalchemy"),
]


@pytest.mark.parametrize(
    ("module", "name", "needs"), EXAMPLES, ids=[e[0] for e in EXAMPLES]
)
def test_example_builds(module: str, name: str, needs: str | None):
    if needs:
        pytest.importorskip(needs)

    dispatcher_cls = getattr(importlib.import_module(module), name)
    dispatcher = dispatcher_cls(token="123456:TEST-token")

    assert isinstance(dispatcher, BaseDispatcher)
    assert dispatcher.used_update_types()  # хендлеры собраны, allowed_updates не пуст


def test_chestor_routers_tree_builds():
    # Дерево из 47 роутеров без хендлеров: проверяем только сборку дерева.
    from examples.chestor_routers.dispatcher import AppDispatcher

    assert len(list(AppDispatcher(token="123456:TEST-token").children)) > 0


async def feed(dispatcher, raw):
    from .conftest import bind

    await dispatcher._handle(dispatcher.create_context(bind(raw, dispatcher.api)))


async def test_filtered_bot_private_and_group(telegram):
    from examples.filtered_bot import Dispatcher

    from .conftest import message_update

    dp = Dispatcher(token="123456:TEST-token")
    await feed(dp, message_update("привет", uid=7))
    await feed(dp, message_update("привет", uid=7, chat=-100))
    assert [m["text"] for m in telegram.sent] == [
        "Только между нами: привет",
        "В группах я не эхо-бот, напиши мне в личку.",
    ]
    await dp.api.close_session()


async def test_db_bot_counts_messages_per_user(telegram, tmp_path, monkeypatch):
    pytest.importorskip("sqlalchemy")
    from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

    from examples import db_bot

    from .conftest import message_update

    engine = create_async_engine(f"sqlite+aiosqlite:///{tmp_path / 'test.sqlite3'}")
    monkeypatch.setattr(db_bot, "engine", engine)
    monkeypatch.setattr(
        db_bot, "session_factory", async_sessionmaker(engine, expire_on_commit=False)
    )

    dp = db_bot.Dispatcher(token="123456:TEST-token")
    await dp.on_startup()
    for _ in range(2):
        await feed(dp, message_update("привет", uid=7))
    await feed(dp, message_update("привет", uid=8))

    assert [m["text"] for m in telegram.sent] == [
        "Сообщений от тебя: 1",
        "Сообщений от тебя: 2",
        "Сообщений от тебя: 1",  # у другого пользователя свой счёт
    ]
    await dp.on_shutdown()
    await dp.api.close_session()


async def test_data_parsed_bot_answers_and_explains_mistakes(telegram):
    from examples.data_parsed_bot import Dispatcher

    from .conftest import message_update

    dp = Dispatcher(token="123456:TEST-token")
    for text in [
        "/calc 2 + 3",
        "/calc 6 / 0",
        "/calc 2 + x",
        "/calc",
        "/say 2 привет  мир",
        "/say",
        "/say x",
        "/transfer @vasya 100",
        "Кинуть @vasya 5",
        "перевести @vasya",
        "/перевести @vasya 1",
    ]:
        await feed(dp, message_update(text))

    answers = [m["text"] for m in telegram.sent]
    assert answers[0] == "2 + 3 = 5"
    assert answers[1] == "6 / 0 = на ноль делить нельзя"
    assert (
        answers[2]
        == "Не получилось: нужно целое число.\nНужно: /calc <one> <operator: +|-|*|/> <two>"
    )
    assert answers[3].startswith("Не получилось: не хватает аргумента")
    assert answers[4] == "привет  мир\nпривет  мир"
    assert answers[5] == "Что сказать?"
    assert answers[6].endswith("Нужно: /say [times] [text...]")
    assert answers[7] == "Переведено 100 для @vasya (transfer)"
    assert answers[8] == "Переведено 5 для @vasya (кинуть)"  # регистр не важен
    assert answers[9].endswith("Нужно: перевести <to> <amount>")  # слово, которым позвали
    assert len(answers) == 10  # «/перевести» с префиксом не подходит: тишина
    await dp.api.close_session()


async def test_reply_bot_every_command(telegram):
    from examples.reply_bot import HELP, Dispatcher

    from .conftest import REPLY_SAMPLES, reply_update

    hint = "Не то сообщение для этой команды.\n\n" + HELP
    user = REPLY_SAMPLES["user"]["from"]
    bold = {"type": "bold", "offset": 0, "length": 1}
    italic = {"type": "italic", "offset": 2, "length": 1}
    file = {"file_id": "a", "file_unique_id": "b"}
    small = {**file, "width": 10, "height": 10}
    big = {**file, "width": 100, "height": 50}

    cases = [
        # 1. готовое условие
        ("/warn флуд", {"from": user}, "Предупреждение: Петя (id 99), флуд"),
        ("/warn", {"from": user}, "Предупреждение: Петя (id 99), без причины"),
        ("/warn", {"from": {**user, "id": 5, "is_bot": True}}, "Ботов не предупреждаем."),
        ("/warn флуд", {}, hint),  # ответ есть, автора нет
        ("/warn флуд", None, hint),  # не ответ
        ("/text", {"text": "раз два три"}, "Символов: 11, слов: 3."),
        ("/text", REPLY_SAMPLES["sticker"], hint),  # ответ не на текст
        ("/entities", {"text": "a b c", "entities": [bold, bold, italic]}, "В тексте: bold: 2, italic: 1."),
        ("/entities", {"caption": "x", "caption_entities": [italic]}, "В подписи: italic: 1."),
        ("/entities", {"text": "без форматирования"}, hint),
        (
            "/sticker",
            {"sticker": {**REPLY_SAMPLES["sticker"]["sticker"], "emoji": "😀", "set_name": "cats"}},
            "Стикер 😀 из набора cats.",
        ),
        ("/sticker", REPLY_SAMPLES["sticker"], "Стикер ? из набора без имени."),
        (
            "/file",
            {"document": {**file, "file_name": "a.pdf", "mime_type": "application/pdf", "file_size": 2048}},
            "Файл a.pdf, application/pdf, 2.0 КБ.",
        ),
        ("/file", REPLY_SAMPLES["document"], "Файл без имени, ?, ?."),
        # 2. несколько условий сразу
        ("/photo", {"photo": [small, big], "from": user}, "Фото 100x50 от Петя."),
        ("/photo", {"photo": [small]}, hint),  # фото есть, автора нет
        ("/caption", {"photo": [small, big], "caption": "закат"}, "Подпись: закат. Размеров фото: 2."),
        ("/caption", {"photo": [small]}, hint),  # подписи нет
        # 3. любое из и обычный if
        ("/duration", REPLY_SAMPLES["voice"], "Длится 1 с."),
        ("/duration", {"video_note": {**file, "length": 1, "duration": 3}}, "Длится 3 с."),
        ("/duration", {"animation": {**file, "width": 1, "height": 1, "duration": 9}}, "Длится 9 с."),
        ("/duration", {"text": "текст"}, hint),
        ("/who", {"from": user}, "Это Петя (id 99)."),
        ("/who", {}, "Автор неизвестен (сообщение из канала или анонимное)."),
        ("/who", None, "Ответьте командой на чьё-нибудь сообщение."),
        # 4. подсказки
        ("/help", None, HELP),
        ("/start", None, HELP),
    ]

    dp = Dispatcher(token="123456:TEST-token")
    for text, replied, expected in cases:
        telegram.clear()
        await feed(dp, reply_update(text, replied))
        assert [m["text"] for m in telegram.sent] == [expected], (text, replied)

    telegram.clear()
    await feed(dp, reply_update("просто текст", REPLY_SAMPLES["text"]))
    assert telegram.sent == []  # обычный текст боту не интересен
    await dp.api.close_session()


async def test_download_bot_saves_and_resaves(telegram, monkeypatch, tmp_path):
    from aiohttp import web

    from examples.download_bot import Dispatcher

    from .conftest import message_update

    monkeypatch.chdir(tmp_path)  # downloads/ создаётся рядом с процессом
    telegram.on(
        "getFile", {"file_id": "F", "file_unique_id": "U", "file_path": "docs/a.pdf"}
    )
    telegram.set_file("docs/a.pdf", b"pdf-content")

    dp = Dispatcher(token="123456:TEST-token")

    await feed(dp, message_update("/save"))  # ни файла, ни ответа на файл
    assert telegram.sent[-1]["text"].startswith("Пришлите файл")
    assert list((tmp_path / "downloads").iterdir()) == []  # папка есть, файла — нет

    await feed(
        dp,
        message_update(
            "/save", document={"file_id": "F", "file_unique_id": "U"}
        ),
    )
    assert telegram.sent[-1]["text"] == "Сохранил 11 байт в downloads/1.pdf."
    assert (tmp_path / "downloads" / "1.pdf").read_bytes() == b"pdf-content"

    # /save со своим именем: overwrite=False, второй раз с тем же именем не затирает первый.
    for expected in ("downloads/report.pdf", "downloads/report (1).pdf"):
        await feed(
            dp,
            message_update(
                "/save report", document={"file_id": "F", "file_unique_id": "U"}
            ),
        )
        assert telegram.sent[-1]["text"] == f"Сохранил 11 байт в {expected}."
    assert {p.name for p in (tmp_path / "downloads").iterdir()} == {
        "1.pdf",
        "report.pdf",
        "report (1).pdf",
    }

    await feed(dp, message_update("/resave F"))
    assert telegram.sent[-1]["text"] == "Сохранил 11 байт в downloads/resaved-1.pdf."
    assert (tmp_path / "downloads" / "resaved-1.pdf").read_bytes() == b"pdf-content"

    telegram.on(
        "getFile",
        lambda body: web.json_response(
            {"ok": False, "error_code": 400, "description": "Bad Request: wrong id"}
        ),
    )
    await feed(dp, message_update("/resave чужой-id"))
    assert telegram.sent[-1]["text"] == "Такой file_id скачать не получилось."

    await dp.api.close_session()


async def test_deferred_bot_secret_remind_report(telegram, monkeypatch):
    import asyncio

    from examples import deferred_bot

    from .conftest import message_update

    monkeypatch.setattr(deferred_bot, "SECRET_TTL", 0.05)
    monkeypatch.setattr(deferred_bot, "REPORT_SECONDS", 0.05)
    dp = deferred_bot.Dispatcher(token="123456:TEST-token")

    async def settle():
        async with asyncio.timeout(2):
            while dp._background.active:
                await asyncio.sleep(0.01)

    await feed(dp, message_update("/secret"))
    assert telegram.methods() == [
        "sendMessage"
    ]  # хендлер ответил и закончил, удаление ещё впереди
    await settle()
    assert telegram.methods() == ["sendMessage", "deleteMessage"]

    telegram.clear()
    await feed(dp, message_update("/remind 0 позвонить маме"))
    await settle()
    assert [m["text"] for m in telegram.sent] == [
        "Напомню через 0 с",
        "⏰ Напоминание: позвонить маме",
    ]

    telegram.clear()
    await feed(dp, message_update("/remind x"))
    assert telegram.sent[-1]["text"] == "Нужно: /remind <seconds> <text...>"

    telegram.clear()
    await feed(dp, message_update("/report"))
    assert telegram.methods() == ["sendMessage"]
    await settle()
    assert telegram.methods() == ["sendMessage", "editMessageText"]
    assert telegram.last()[1]["text"] == "✅ Отчёт готов"
    await dp.api.close_session()
