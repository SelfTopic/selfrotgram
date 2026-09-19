from dataclasses import dataclass
from typing import Any, TypeVar

from ..client import Bot
from ..types import Update
from .accessors import TEvent
from .methods import ContextMethods

TContext = TypeVar("TContext", bound="BaseContext[Any]")


@dataclass
class BaseContext(ContextMethods[TEvent]):
    update: Update
    bot: Bot
