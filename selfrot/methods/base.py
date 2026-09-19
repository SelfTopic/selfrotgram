import dataclasses
from typing import Any, ClassVar, Generic, TypeVar, cast

from pydantic import BaseModel

from ..types import InputFile

TResult = TypeVar("TResult")


def _serialize(value: Any) -> Any:
    if isinstance(value, InputFile):
        return value
    if isinstance(value, BaseModel):
        return value.model_dump(mode="json", by_alias=True, exclude_none=True)
    if isinstance(value, (list, tuple)):
        return [_serialize(item) for item in value]

    return value


class TelegramMethod(Generic[TResult]):
    """
    Метод Bot API. Наследники (methods/generated.py) — dataclass'ы с
    аргументами метода; TResult — то, что вернёт Telegram (__returning__).
    """

    __api_method__: ClassVar[str]
    __returning__: ClassVar[Any]

    def to_payload(self) -> dict[str, Any]:
        """Аргументы, которые заданы (None пропускаем; False и 0 — нет)."""
        payload: dict[str, Any] = {}
        for field in dataclasses.fields(cast(Any, self)):
            value = getattr(self, field.name)
            if value is not None:
                payload[field.name] = _serialize(value)

        return payload
