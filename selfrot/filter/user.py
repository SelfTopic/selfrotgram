from typing import Any

from ..context import BaseContext
from .base import BaseFilter


class FromUser(BaseFilter[BaseContext[Any]]):
    """
    Отправитель события — один из перечисленных пользователей: автор сообщения,
    нажавший кнопку, участник, чей статус изменился. Подходит любому виду
    обработчика; у события без пользователя (пост канала, анонимный админ) не
    совпадает.

        FromUser(*settings.ADMIN_IDS)            # как CreatorMiddleware, но фильтром
        FromUser(42) & Command("ban")
        ~FromUser(*BANNED)
    """

    def __init__(self, *user_ids: int) -> None:
        self.user_ids = frozenset(user_ids)

    async def check(self, ctx: BaseContext[Any]) -> bool:
        user = ctx.user
        return user is not None and user.id in self.user_ids

    def __repr__(self) -> str:
        return f"FromUser({', '.join(map(str, sorted(self.user_ids)))})"
