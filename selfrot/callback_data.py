from enum import Enum
from typing import TYPE_CHECKING, Any, ClassVar, Self, get_args

from pydantic import BaseModel, ValidationError

from .exceptions import CallbackDataError, DefinitionError

if TYPE_CHECKING:
    from .filter.callback import CallbackPayloadFilter

MAX_BYTES = 64  # лимит Telegram на callback_data


def _encode(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "1" if value else "0"
    if isinstance(value, Enum):
        return str(value.value)

    return str(value)


class CallbackPayload(BaseModel):
    """
    Типизированные данные кнопки. Вместо f"duel:{id}:{action}:{uid}" и ручного
    разбора split(":"):

        class Duel(CallbackPayload, prefix="duel"):
            duel_id: int
            action: Literal["accept", "decline"]
            expected_id: int

        button("Принять", Duel(duel_id=1, action="accept", expected_id=5))
        # callback_data == "duel:1:accept:5"

        class Accept(CallbackQueryHandler[AppContext[DataCallbackQuery]]):
            duel = Duel.filter(action="accept")
            query = duel

            async def handle(self):
                data = self.duel.parse(self.ctx)   # Duel, типы уже проверены

    Поля упаковываются в порядке объявления через sep (по умолчанию ":"). Допустимы
    str, int, bool, Enum, Literal и Optional (None — пустое поле). Значение с sep
    внутри, а также больше 64 байт в итоге — CallbackDataError при pack(), а не 400
    от Telegram при отправке.
    """

    __prefix__: ClassVar[str]
    __sep__: ClassVar[str]

    def __init_subclass__(cls, *, prefix: str, sep: str = ":", **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        if not prefix or not sep or sep in prefix:
            raise DefinitionError(
                f"{cls.__name__}: prefix не пустой и без разделителя {sep!r} внутри"
            )

        cls.__prefix__ = prefix
        cls.__sep__ = sep

    def pack(self) -> str:
        sep = self.__sep__
        parts = [self.__prefix__]
        for name in type(self).model_fields:
            text = _encode(getattr(self, name))
            if sep in text:
                raise CallbackDataError(
                    f"{type(self).__name__}.{name}={text!r}: внутри значения "
                    f"разделитель {sep!r}"
                )
            parts.append(text)

        data = sep.join(parts)
        size = len(data.encode())
        if size > MAX_BYTES:
            raise CallbackDataError(
                f"{type(self).__name__}: callback_data {size} байт, максимум "
                f"{MAX_BYTES} ({data!r})"
            )

        return data

    @classmethod
    def unpack(cls, data: str) -> Self:
        sep = cls.__sep__
        head, *rest = data.split(sep)
        fields = cls.model_fields
        if head != cls.__prefix__ or len(rest) != len(fields):
            raise CallbackDataError(f"{data!r} не подходит под {cls.__name__}")

        raw: dict[str, Any] = {}
        for (name, field), text in zip(fields.items(), rest, strict=True):
            optional = type(None) in get_args(field.annotation)
            raw[name] = None if text == "" and optional else text

        try:
            return cls.model_validate(raw)
        except ValidationError as e:
            raise CallbackDataError(f"{data!r}: {cls.__name__}: {e}") from e

    @classmethod
    def try_unpack(cls, data: str) -> Self | None:
        try:
            return cls.unpack(data)
        except CallbackDataError:
            return None

    @classmethod
    def filter(cls, **equals: Any) -> "CallbackPayloadFilter[Self]":
        """Фильтр: данные кнопки этого класса, у которых указанные поля равны."""
        from .filter.callback import CallbackPayloadFilter

        return CallbackPayloadFilter(cls, **equals)
