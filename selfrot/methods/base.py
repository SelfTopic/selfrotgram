import dataclasses
from typing import Any, ClassVar, Generic, TypeVar, cast

from pydantic import BaseModel

from ..types import InputFile

TResult = TypeVar("TResult")


class _Attachments:
    """
    Файлы внутри объектов (InputMediaPhoto.media=InputFile(...)): каждому — своё
    имя части multipart, в JSON вместо файла — «attach://<имя>». Один и тот же
    объект в двух местах загружается один раз.
    """

    def __init__(self, taken: set[str]) -> None:
        self.files: dict[str, InputFile] = {}
        self._names: dict[int, str] = {}
        self._taken = taken  # имена аргументов метода: часть не должна их перекрыть

    def attach(self, file: InputFile) -> str:
        name = self._names.get(id(file))
        if name is None:
            index = len(self.files)
            while (name := f"file{index}") in self._taken or name in self.files:
                index += 1
            self._names[id(file)] = name
            self.files[name] = file

        return f"attach://{name}"


def _attach(value: Any, attachments: _Attachments) -> Any:
    if isinstance(value, InputFile):
        return attachments.attach(value)
    if isinstance(value, dict):
        return {key: _attach(item, attachments) for key, item in value.items()}
    if isinstance(value, list):
        return [_attach(item, attachments) for item in value]

    return value


def _serialize(value: Any, attachments: _Attachments) -> Any:
    if isinstance(value, InputFile):
        return value  # аргумент верхнего уровня — сам по себе часть multipart
    if isinstance(value, BaseModel):
        # mode="python" оставляет InputFile объектом (в JSON он не превращается);
        # всё остальное в типах Telegram — и так JSON-значения.
        dumped = value.model_dump(by_alias=True, exclude_none=True)
        return _attach(dumped, attachments)
    if isinstance(value, (list, tuple)):
        return [_serialize(item, attachments) for item in value]

    return value


class TelegramMethod(Generic[TResult]):
    """
    Метод Bot API. Наследники (methods/generated.py) — dataclass'ы с
    аргументами метода; TResult — то, что вернёт Telegram (__returning__).
    """

    __api_method__: ClassVar[str]
    __returning__: ClassVar[Any]

    def to_payload(self) -> dict[str, Any]:
        """
        Аргументы, которые заданы (None пропускаем; False и 0 — нет). Файлы из
        объектов добавляются отдельными ключами (file0, file1…), на которые
        ссылаются их attach://.
        """
        fields = dataclasses.fields(cast(Any, self))
        attachments = _Attachments({field.name for field in fields})
        payload: dict[str, Any] = {}
        for field in fields:
            value = getattr(self, field.name)
            if value is not None:
                payload[field.name] = _serialize(value, attachments)

        payload.update(attachments.files)
        return payload
