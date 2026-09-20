from importlib.metadata import PackageNotFoundError, version

from .callback_data import CallbackPayload
from .client import Bot, BotDefaults
from .command_args import CommandArgs, Rest
from .context import BaseContext, TEvent
from .deferred import Deferred
from .dispatcher import BaseDispatcher
from .fsm import MemoryStorage, State, States
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
    "CallbackPayload",
    "CommandArgs",
    "Deferred",
    "InlineKeyboard",
    "MemoryStorage",
    "MessageHandler",
    "Rest",
    "State",
    "States",
    "TEvent",
    "__version__",
    "button"
]
