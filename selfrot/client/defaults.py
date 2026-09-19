import dataclasses
from dataclasses import dataclass
from typing import Any, TypeVar

from pydantic import BaseModel

from ..types import LinkPreviewOptions

T = TypeVar("T")


@dataclass(frozen=True, kw_only=True)
class BotDefaults:
    """
    Значения, которые подставляются в каждый вызов, где аргумент не задан (None):

        class MyBot(Bot):
            defaults = BotDefaults(
                parse_mode="HTML",
                link_preview_options=LinkPreviewOptions(is_disabled=True),
            )

    Подстановка идёт по имени поля и в аргументы метода, и в объекты внутри них
    (InputMedia*, InputTextMessageContent, результаты inline-запросов). Явно
    заданное в вызове всегда сильнее: link_preview_options заменяется целиком, а
    булевы (disable_notification=False) перекрывают умолчание. Единственное, что
    нельзя «выключить» на один вызов, — parse_mode: значения «без разметки»
    у Telegram нет, поэтому текст в таком вызове надо экранировать.
    """

    parse_mode: str | None = None
    link_preview_options: LinkPreviewOptions | None = None
    disable_notification: bool | None = None
    protect_content: bool | None = None
    show_caption_above_media: bool | None = None

    def values(self) -> dict[str, Any]:
        found = {f.name: getattr(self, f.name) for f in dataclasses.fields(self)}
        return {name: value for name, value in found.items() if value is not None}

    def apply(self, value: T) -> T:
        """Копия value с подставленными умолчаниями (сам value не меняется)."""
        values = self.values()
        return _apply(value, values) if values else value


def _field_names(value: Any) -> list[str] | None:
    if isinstance(value, BaseModel):
        return list(type(value).model_fields)
    if dataclasses.is_dataclass(value) and not isinstance(value, type):
        return [f.name for f in dataclasses.fields(value)]

    return None


def _apply(value: Any, values: dict[str, Any]) -> Any:
    if isinstance(value, (list, tuple)):
        items = [_apply(item, values) for item in value]
        if all(new is old for new, old in zip(items, value, strict=True)):
            return value

        return type(value)(items)

    names = _field_names(value)
    if names is None:
        return value

    updates: dict[str, Any] = {}
    for name in names:
        current = getattr(value, name)
        if current is None:
            if name in values:
                updates[name] = values[name]
        else:
            new = _apply(current, values)
            if new is not current:
                updates[name] = new

    if not updates:
        return value
    if isinstance(value, BaseModel):
        return value.model_copy(update=updates)

    return dataclasses.replace(value, **updates)
