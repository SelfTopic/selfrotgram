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
