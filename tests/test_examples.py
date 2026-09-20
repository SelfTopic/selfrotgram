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
