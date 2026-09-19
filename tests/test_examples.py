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
