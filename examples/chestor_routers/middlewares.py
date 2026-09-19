from typing import Optional

from selfrot import BaseContext, BaseMiddleware


class _PassThrough(BaseMiddleware[BaseContext]):
    async def pre_handle(self) -> bool:
        return True

    async def post_handle(self, exc: Optional[BaseException] = None) -> None:
        return None


# Глобальные (в chestor_bot: dp.update.middleware) — на каждый апдейт.
class DatabaseMiddleware(_PassThrough):
    """Заглушка. Логика: сессия БД на апдейт (см. examples/db_bot.py)."""


class SyncEntitiesMiddleware(_PassThrough):
    """Заглушка. Логика: апсерт User/Chat (см. examples/bot_command)."""


class BanMiddleware(_PassThrough):
    """Заглушка. Логика: забаненных не пускаем дальше."""


# На роутерах (в chestor_bot: Router.message/callback_query.middleware) —
# только вокруг хендлера из своей ветки.
class ModeratorMiddleware(_PassThrough):
    """Заглушка. Логика: только админы супергруппы."""


class GhoulMiddleware(_PassThrough):
    """Заглушка. Логика: пользователь зарегистрирован гулем и жив."""


class CreatorMiddleware(_PassThrough):
    """Заглушка. Логика: только создатель бота."""


class RpCommandsMiddleware(_PassThrough):
    """Заглушка. Логика: прогрев кеша RP-команд чата."""
