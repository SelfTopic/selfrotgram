import types
from functools import cache
from typing import TypeGuard, TypeVar, Union, get_args, get_origin, get_type_hints

from pydantic import BaseModel

from ..exceptions import DefinitionError
from ..types import Message

# Модуль сгенерированных типов Bot API: корень суженного типа лежит в нём.
_GENERATED_MODULE = Message.__module__


def _is_optional(annotation: object) -> bool:
    is_union = get_origin(annotation) in (Union, types.UnionType)
    return is_union and type(None) in get_args(annotation)


def is_bot_api_type(model: object) -> TypeGuard[type[BaseModel]]:
    return (
        isinstance(model, type)
        and issubclass(model, BaseModel)
        and any(base.__module__ == _GENERATED_MODULE for base in model.__mro__)
    )


def root_type(model: type[BaseModel]) -> type[BaseModel]:
    """Тип Bot API, от которого сужен model (TextMessage -> Message)."""
    for base in model.__mro__:
        if base.__module__ == _GENERATED_MODULE and issubclass(base, BaseModel):
            return base

    raise DefinitionError(
        f"{model.__name__} не наследует тип Bot API из {_GENERATED_MODULE}"
    )


def _without_none(annotation: object) -> object:
    if not _is_optional(annotation):
        return annotation

    rest = [a for a in get_args(annotation) if a is not type(None)]
    return rest[0] if len(rest) == 1 else annotation


def _resolve(model: type[BaseModel], annotation: object) -> object:
    """
    Аргумент обобщённого суженного типа. Reply[PhotoCaption] хранит его в метаданных
    pydantic, а get_type_hints отдаёт неразрешённый TypeVar.
    """
    if not isinstance(annotation, TypeVar):
        return annotation

    for base in model.__mro__:
        meta = getattr(base, "__pydantic_generic_metadata__", None)
        if not meta or meta["origin"] is None:
            continue

        parameters = meta["origin"].__pydantic_generic_metadata__["parameters"]
        if annotation in parameters:
            return meta["args"][parameters.index(annotation)]

    return annotation


@cache
def required_fields(model: type[BaseModel]) -> frozenset[str]:
    """
    Что model обещает сверх корневого типа: имена полей, которые корень допускает
    пустыми, а model уже нет («text»), и пути во вложенных суженных типах
    («reply_to_message.user» для Reply[UserMessage]). Считается по типам
    (get_type_hints собирает MRO так же, как type checker), а не по model_fields:
    у pydantic при множественном наследовании сужение от второй базы теряется.
    """
    root = root_type(model)
    root_hints = get_type_hints(root)
    hints = get_type_hints(model)

    paths: set[str] = set()
    for name in root.model_fields:
        wanted = _resolve(model, hints[name])
        if _is_optional(root_hints[name]) and not _is_optional(wanted):
            paths.add(name)

        # Само поле может быть суженным типом: reply_to_message: UserMessage.
        original, nested = _without_none(root_hints[name]), _without_none(wanted)
        if (
            nested is not original
            and is_bot_api_type(nested)
            and root_type(nested) is original
        ):
            paths.add(name)
            paths |= {f"{name}.{path}" for path in required_fields(nested)}

    return frozenset(paths)
