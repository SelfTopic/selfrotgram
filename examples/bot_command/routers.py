from selfrot import BaseRouter

from .context import AppContext
from .handlers import BotHandler


class BotRouter(BaseRouter[AppContext]):
    handlers = (BotHandler,)


router = BotRouter
