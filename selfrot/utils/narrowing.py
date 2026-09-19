import types
from functools import cache
from typing import Union, get_args, get_origin, get_type_hints

from pydantic import BaseModel

from ..exceptions import DefinitionError
from ..types import Message

# Модуль сгенерированных типов Bot API: корень суженного типа лежит в нём.
_GENERATED_MODULE = Message.__module__


def _is_optional(annotation: object) -> bool:
    is_union = get_origin(annotation) in (Union, types.UnionType)
    return is_union and type(None) in get_args(annotation)


def is_bot_api_type(model: object) -> bool:
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


@cache
def required_fields(model: type[BaseModel]) -> frozenset[str]:
    """
    Поля, которые корневой тип допускает пустыми, а model уже нет.
    Считается по типам (get_type_hints собирает MRO так же, как type checker),
    а не по model_fields: у pydantic при множественном наследовании
    сужение от второй базы теряется.
    """
    root = root_type(model)
    root_hints = get_type_hints(root)
    hints = get_type_hints(model)

    return frozenset(
        name
        for name in root.model_fields
        if _is_optional(root_hints[name]) and not _is_optional(hints[name])
    )
