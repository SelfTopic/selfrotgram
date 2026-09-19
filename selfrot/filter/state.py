from typing import Any

from ..context import BaseContext
from ..fsm import State, States
from .base import BaseFilter


class InState(BaseFilter[BaseContext[Any]]):
    """
    Пользователь сейчас в одном из состояний: конкретном или в любом из группы.

        InState(Register.age)
        InState(Register)                    # любой шаг сценария
        InState(Register.name, Register.age)

    Подходит любому виду обработчика. Первый подошедший хендлер забирает апдейт, так
    что ответ на шаг диалога нужно ставить выше общих обработчиков текста.
    """

    def __init__(self, *targets: State[Any] | type[States]) -> None:
        names: set[str] = set()
        for target in targets:
            if isinstance(target, State):
                names.add(target.name)
            else:
                names.update(state.name for state in target.all())

        self.names = frozenset(names)

    async def check(self, ctx: BaseContext[Any]) -> bool:
        return await ctx.fsm.state() in self.names

    def __repr__(self) -> str:
        return f"InState({', '.join(sorted(self.names))})"


class NoState(BaseFilter[BaseContext[Any]]):
    """У пользователя нет активного диалога."""

    async def check(self, ctx: BaseContext[Any]) -> bool:
        return await ctx.fsm.state() is None
