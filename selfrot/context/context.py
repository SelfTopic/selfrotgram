import inspect
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, TypeVar

from ..client import Bot
from ..deferred import BackgroundTasks, Deferred
from ..exceptions import ContextError, DefinitionError
from ..fsm import FSM
from ..types import Update
from .accessors import TEvent
from .methods import ContextMethods

if TYPE_CHECKING:
    from ..handlers.base import BaseHandler

TContext = TypeVar("TContext", bound="BaseContext[Any]")


@dataclass
class BaseContext(ContextMethods[TEvent]):
    update: Update
    bot: Bot
    # Прикрепляет диспетчер. Не аргумент конструктора: пользовательские контексты
    # собираются как self.context(update, api, сервисы...) и ничего не замечают.
    _fsm: FSM | None = field(default=None, init=False, repr=False, compare=False)

    # Отложенные вызовы этого апдейта и реестр диспетчера (прикрепляет диспетчер).
    _deferred: list[Deferred] = field(
        default_factory=list, init=False, repr=False, compare=False
    )
    _background: BackgroundTasks | None = field(
        default=None, init=False, repr=False, compare=False
    )

    def defer(
        self,
        fn: Callable[..., Awaitable[Any]],
        *args: Any,
        delay: float = 0.0,
        owner: "BaseHandler[Any] | None" = None,
        **kwargs: Any,
    ) -> Deferred:
        """
        Вызвать async-функцию позже, после закрытия хендлера и мидлварей, через delay
        секунд. Для хендлера удобнее self.defer(...): ошибка тогда пойдёт в его on_error.
        """
        if self._background is None:
            raise ContextError(
                "У контекста нет реестра отложенных вызовов: он создан не диспетчером"
            )
        if not inspect.iscoroutinefunction(fn):
            raise DefinitionError(
                f"defer() принимает async-функцию (у неё await), получено {fn!r}"
            )
        if delay < 0:
            raise DefinitionError(
                f"defer(): delay не может быть отрицательным ({delay})"
            )

        deferred = Deferred(fn, args, kwargs, delay, ctx=self, owner=owner)
        self._background.register(deferred)  # DeferredLimitError, если места нет
        self._deferred.append(deferred)
        return deferred

    @property
    def fsm(self) -> FSM:
        """Состояние диалога этого пользователя в этом чате."""
        if self._fsm is None:
            raise ContextError(
                "У контекста нет FSM: он создан не диспетчером "
                "(в тесте прикрепите FSM(storage, key) к ctx._fsm)"
            )

        return self._fsm
