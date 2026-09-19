from copy import copy
from typing import Any, Generic, TypeVar

from ..callback_data import CallbackPayload
from ..context import BaseContext
from ..exceptions import DefinitionError, FilterMatchError
from ..types import CallbackQuery, DataCallbackQuery
from .base import BaseFilter
from .strings import Contains, Endswith, Equals, Regexp, Startswith, StringFilter

TPayload = TypeVar("TPayload", bound=CallbackPayload)


class CallbackDataSource(StringFilter):
    """Данные кнопки (callback_query.data). Гарантирует DataCallbackQuery."""

    guarantees = DataCallbackQuery

    def _read(self, ctx: BaseContext[Any]) -> str | None:
        event = ctx.event
        return event.data if isinstance(event, CallbackQuery) else None


class CallbackData(Equals, CallbackDataSource):
    """data равна образцу: CallbackData("imut")."""


class CallbackDataStartswith(Startswith, CallbackDataSource):
    """data начинается с образца: CallbackDataStartswith("mut:")."""


class CallbackDataEndswith(Endswith, CallbackDataSource):
    """data заканчивается образцом."""


class CallbackDataContains(Contains, CallbackDataSource):
    """data содержит образец."""


class CallbackDataRegexp(Regexp, CallbackDataSource):
    """data подходит под выражение; match(ctx) отдаёт совпадение."""


class CallbackPayloadFilter(
    BaseFilter[BaseContext[DataCallbackQuery]], Generic[TPayload]
):
    """
    Данные кнопки разобрались в payload (префикс, число и типы полей), и указанные
    поля равны заданным. Создаётся через Payload.filter(action="accept").

    Разобранный объект в фильтре не хранится (он общий для всех апдейтов): в
    хендлере его берут явно, parse(ctx).
    """

    guarantees = DataCallbackQuery

    def __init__(self, payload: type[TPayload], **equals: Any) -> None:
        unknown = set(equals) - set(payload.model_fields)
        if unknown:
            raise DefinitionError(
                f"{payload.__name__}.filter(): нет полей {sorted(unknown)}; "
                f"есть {list(payload.model_fields)}"
            )

        self.payload = payload
        self.equals = equals
        self.owner_field: str | None = None

    def pressed_by(self, field: str) -> "CallbackPayloadFilter[TPayload]":
        """
        Копия фильтра, которая пропускает только нажатие пользователя, чей id лежит
        в поле field (кнопку в группе видят все, а нажать может только тот, для кого
        она). Чужое нажатие не совпадает: следующим хендлером ловят его и отвечают:

            mine = Duel.filter(action="accept").pressed_by("expected_id")   # хендлер 1
            other = Duel.filter(action="accept")                             # хендлер 2: «не для тебя»
        """
        if field not in self.payload.model_fields:
            raise DefinitionError(
                f"{self.payload.__name__}.filter().pressed_by({field!r}): нет такого "
                f"поля; есть {list(self.payload.model_fields)}"
            )

        clone = copy(self)
        clone.owner_field = field
        return clone

    def _find(self, ctx: BaseContext[Any]) -> TPayload | None:
        event = ctx.event
        if not isinstance(event, CallbackQuery) or event.data is None:
            return None

        found = self.payload.try_unpack(event.data)
        if found is None:
            return None

        for name, expected in self.equals.items():
            if getattr(found, name) != expected:
                return None

        if self.owner_field is not None:
            user = ctx.user
            if user is None or getattr(found, self.owner_field) != user.id:
                return None

        return found

    async def check(self, ctx: BaseContext[Any]) -> bool:
        return self._find(ctx) is not None

    def parse(self, ctx: BaseContext[Any]) -> TPayload:
        """Данные кнопки. Только после того, как check() сказал да."""
        found = self._find(ctx)
        if found is None:
            raise FilterMatchError(f"{self!r} не подошёл к этому апдейту")

        return found

    def __repr__(self) -> str:
        args = ", ".join(f"{k}={v!r}" for k, v in self.equals.items())
        owner = f".pressed_by({self.owner_field!r})" if self.owner_field else ""
        return f"{self.payload.__name__}.filter({args}){owner}"
