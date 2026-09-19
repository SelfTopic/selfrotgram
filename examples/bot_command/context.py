from dataclasses import dataclass

from selfrot import BaseContext, TEvent

from .services import DialogService


@dataclass
class AppContext(BaseContext[TEvent]):
    dialogs: DialogService
