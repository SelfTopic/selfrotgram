from selfrot import BaseDispatcher, Bot
from selfrot.types import Update

from .context import AppContext
from .database import create_tables
from .middlewares import SyncUserMiddleware
from .services import DialogService


class AppDispatcher(BaseDispatcher[AppContext]):
    bot = Bot
    context = AppContext
    middlewares = (SyncUserMiddleware,)
    auto_connect = (".routers",)

    def __init__(self, token: str | None = None) -> None:
        super().__init__(token)
        self.dialogs = DialogService()

    def create_context(self, update: Update) -> AppContext:
        return self.context(update, self.api, self.dialogs)

    async def setup(self) -> None:
        await create_tables()
