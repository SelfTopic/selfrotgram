from typing import Any, Optional

from selfrot import BaseMiddleware

from .context import AppContext
from .database import session_factory
from .repositories import UserRepository


class SyncUserMiddleware(BaseMiddleware[AppContext]):
    """
    Апсертит пользователя на каждое сообщение. Своя сессия с немедленным
    commit, а не сессия хендлера: иначе строка users держится залоченной,
    пока хендлер не закончит (тот же довод, что в chestor_bot).
    """

    async def pre_handle(self) -> bool:
        message = self.ctx.message
        if message is None or message.user is None:
            return True

        user = message.user
        async with session_factory() as session:
            await UserRepository(session).upsert(
                telegram_id=user.id,
                first_name=user.first_name,
                last_name=user.last_name,
                username=user.username,
            )
            await session.commit()

        return True

    async def post_handle(self, exc: Optional[BaseException] = None) -> Any:
        return None
