from dataclasses import dataclass, field
from typing import Any, TypeVar

from ..client import Bot
from ..exceptions import ContextError
from ..fsm import FSM
from ..types import Update
from .accessors import TEvent
from .methods import ContextMethods

TContext = TypeVar("TContext", bound="BaseContext[Any]")


@dataclass
class BaseContext(ContextMethods[TEvent]):
    update: Update
    bot: Bot
    # Прикрепляет диспетчер. Не аргумент конструктора: пользовательские контексты
    # собираются как self.context(update, api, сервисы...) и ничего не замечают.
    _fsm: FSM | None = field(default=None, init=False, repr=False, compare=False)

    @property
    def fsm(self) -> FSM:
        """Состояние диалога этого пользователя в этом чате."""
        if self._fsm is None:
            raise ContextError(
                "У контекста нет FSM: он создан не диспетчером "
                "(в тесте прикрепите FSM(storage, key) к ctx._fsm)"
            )

        return self._fsm
