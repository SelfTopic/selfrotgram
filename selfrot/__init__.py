from importlib.metadata import PackageNotFoundError, version

from .callback_data import CallbackPayload
from .client import Bot, BotDefaults
from .fsm import MemoryStorage, State, States
from .context import BaseContext, TEvent
from .dispatcher import BaseDispatcher
from .handlers import BaseHandler, MessageHandler
from .keyboard import InlineKeyboard, button
from .middleware import BaseMiddleware
from .router import BaseRouter

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
    "Bot",
    "BotDefaults",
    "State",
    "States",
    "MemoryStorage",
    "CallbackPayload",
    "InlineKeyboard",
    "MessageHandler",
    "TEvent",
    "__version__",
    "button"
]
