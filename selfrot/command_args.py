from typing import Annotated, Any, Literal, get_args, get_origin

from pydantic import BaseModel

from .exceptions import DefinitionError


class _RestMarker:
    """Метка «остаток строки»: см. Rest."""


# Последнее поле модели, которое забирает всё оставшееся (с сохранением пробелов):
# «бот скажи <любой текст>». Обычные поля делят строку по пробелам.
Rest = Annotated[str, _RestMarker()]


class CommandArgs(BaseModel):
    """
    Форма аргументов команды: поля идут в порядке объявления и есть позиции аргументов.

        class CalcArgs(CommandArgs):
            one: int
            operator: Literal["+", "-", "*", "/"]
            two: int

        cmd = Command("calc", CalcArgs)          # /calc 2 + 3

    Типы приводятся из строк (int, float, bool, Enum, Literal), поле со значением по
    умолчанию необязательное и может быть только в конце. Последнее поле типа Rest
    забирает остаток строки целиком. Неверные аргументы дают CommandArgsError.
    """

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any) -> None:
        super().__pydantic_init_subclass__(**kwargs)

        optional_seen = False
        fields = list(cls.model_fields.items())
        for index, (name, field) in enumerate(fields):
            if cls._is_rest(name) and index != len(fields) - 1:
                raise DefinitionError(
                    f"{cls.__name__}.{name}: Rest должен быть последним полем"
                )
            if not field.is_required():
                optional_seen = True
            elif optional_seen:
                raise DefinitionError(
                    f"{cls.__name__}.{name}: обязательное поле после необязательного "
                    "(аргументы позиционные, пропустить средний нельзя)"
                )

    @classmethod
    def _is_rest(cls, name: str) -> bool:
        return any(isinstance(m, _RestMarker) for m in cls.model_fields[name].metadata)

    @classmethod
    def rest_field(cls) -> str | None:
        names = list(cls.model_fields)
        return names[-1] if names and cls._is_rest(names[-1]) else None

    @classmethod
    def positional_fields(cls) -> list[str]:
        rest = cls.rest_field()
        return [name for name in cls.model_fields if name != rest]

    @classmethod
    def usage(cls, command: str) -> str:
        """«/calc <one> <operator: +|-|*|/> <two>»: обязательные в <>, необязательные в []."""
        parts = [command]
        rest = cls.rest_field()
        for name, field in cls.model_fields.items():
            label = name
            annotation = field.annotation
            if get_origin(annotation) is Literal:
                label += ": " + "|".join(str(v) for v in get_args(annotation))
            if name == rest:
                label += "..."
            parts.append(f"<{label}>" if field.is_required() else f"[{label}]")

        return " ".join(parts)
