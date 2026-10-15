from importlib.metadata import PackageNotFoundError, version

from .callback_data import CallbackPayload
from .client import Bot, BotDefaults
from .command_args import CommandArgs, Rest
from .context import BaseContext, TEvent
from .deferred import Deferred
from .dispatcher import BaseDispatcher
from .entities import entity_text, mention_html, mentions
from .fsm import MemoryStorage, State, States
from .handlers import BaseHandler, MessageHandler
from .keyboard import InlineKeyboard, button
from .middleware import BaseMiddleware
from .router import BaseRouter
from .start_payload import StartPayload
from .tasks import BaseTask, Every
from .view import Pagination, View, ViewContent

try:
    __version__ = version("selfrotgram")
except PackageNotFoundError:  # запуск из исходников без установки
    __version__ = "0.0.0+source"

__all__ = [
    "BaseContext",
    "BaseDispatcher",
    "BaseHandler",
    "BaseMiddleware",
    "BaseRouter",
    "BaseTask",
    "Bot",
    "BotDefaults",
    "CallbackPayload",
    "CommandArgs",
    "Deferred",
    "Every",
    "InlineKeyboard",
    "MemoryStorage",
    "MessageHandler",
    "Pagination",
    "Rest",
    "StartPayload",
    "State",
    "States",
    "TEvent",
    "View",
    "ViewContent",
    "__version__",
    "button",
    "entity_text",
    "mention_html",
    "mentions",
]
