from collections.abc import Hashable
from typing import Any

from ..context import BaseContext


def order_by_chat(ctx: BaseContext[Any]) -> Hashable | None:
    """
    Апдейты одного чата идут строго по очереди. Ключ — id чата, а если у апдейта
    чата нет (inline-запрос), то id пользователя.
    """
    chat = ctx.chat
    if chat is not None:
        return chat.id

    return order_by_user(ctx)


def order_by_user(ctx: BaseContext[Any]) -> Hashable | None:
    """Апдейты одного пользователя идут по очереди, а чаты между собой независимы."""
    user = ctx.user
    return user.id if user is not None else None
