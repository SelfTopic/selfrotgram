from dataclasses import dataclass
from typing import Any, Generic, TypeVar, cast, overload

from pydantic import ValidationError

from ..command_args import CommandArgs
from ..context import BaseContext
from ..exceptions import ArgProblem, CommandArgsError, DefinitionError, FilterMatchError
from ..types import Message, TextMessage
from .base import BaseFilter


@dataclass(frozen=True)
class CommandCall:
    """Разбор сообщения с командой."""

    prefix: str
    args: tuple[str, ...]
    rest: str  # всё после команды как написано (без крайних пробелов)


TArgs = TypeVar("TArgs", bound=CommandArgs)
TParsed = TypeVar("TParsed")


class Command(BaseFilter[BaseContext[TextMessage]], Generic[TParsed]):
    """
    /name аргумент аргумент. Имя может быть из нескольких слов, префикс — любым:

        Command("imut", prefixes="/!")           # /imut, !imut
        Command("бот скажи", prefixes="", ignore_case=True)

    prefixes — строка из односимвольных префиксов; "" — команда без префикса.
    Если задан args_count, число аргументов должно совпасть точно, иначе апдейт
    этому хендлеру не подходит.

    Типизированные аргументы: вторым параметром модель CommandArgs. Фильтр совпадает
    по имени команды, а parse(ctx) возвращает модель (числа уже int, оператор из
    Literal) или бросает CommandArgsError: его ловят в on_error и отвечают
    exc.usage. strict=True — неверные аргументы значат «не подходит», а не ошибку
    (апдейт достаётся следующему хендлеру, как с args_count).

        cmd = Command("calc", CalcArgs)
        args = cmd.parse(ctx)                    # CalcArgs

    /name@username (только с префиксом "/") подходит, если username — этого бота
    (Bot.username загружает диспетчер при старте через getMe; пока он неизвестен,
    команды с упоминанием не совпадают).

    Аргументы в хендлере: parse(ctx) — явно, как match(ctx) у регулярных выражений.
    call(ctx) — сырой разбор (префикс, слова, остаток) для обоих вариантов.
    """

    guarantees = TextMessage

    @overload
    def __init__(
        self: "Command[CommandCall]",
        name: str,
        *,
        args_count: int | None = None,
        prefixes: str = "/",
        ignore_case: bool = False,
    ) -> None: ...

    @overload
    def __init__(
        self: "Command[TArgs]",
        name: str,
        args: type[TArgs],
        *,
        strict: bool = False,
        prefixes: str = "/",
        ignore_case: bool = False,
    ) -> None: ...

    def __init__(
        self,
        name: str,
        args: type[CommandArgs] | None = None,
        *,
        args_count: int | None = None,
        strict: bool = False,
        prefixes: str = "/",
        ignore_case: bool = False,
    ) -> None:
        if args is not None and args_count is not None:
            raise DefinitionError(
                f"Command({name!r}): число аргументов берётся из модели, args_count не нужен"
            )

        self.args_model = args
        self.strict = strict
        self.words = tuple(name.split())
        if not self.words:
            raise DefinitionError("Command: пустое имя")
        if name.startswith(tuple(prefixes)):
            raise DefinitionError(f"Command({name!r}): имя пишется без префикса")

        self.name = name
        self.args_count = args_count
        self.prefixes = tuple(prefixes) or ("",)
        self.ignore_case = ignore_case

    def _fold(self, text: str) -> str:
        return text.casefold() if self.ignore_case else text

    def _parse(self, ctx: BaseContext[Any]) -> CommandCall | None:
        message = ctx.event
        if not isinstance(message, Message) or message.text is None:
            return None

        count = len(self.words)
        parts = message.text.split(None, count)
        if len(parts) < count:
            return None

        for prefix in self.prefixes:
            head = parts[0]
            if not head.startswith(prefix):
                continue

            head = head[len(prefix) :]
            if prefix == "/":
                head, _, mention = head.partition("@")
                if mention and not self._is_me(ctx, mention):
                    continue

            written = (head, *parts[1:count])
            if [self._fold(w) for w in written] != [self._fold(w) for w in self.words]:
                continue

            rest = parts[count].rstrip() if len(parts) > count else ""
            args = tuple(rest.split())
            if self.args_count is not None and len(args) != self.args_count:
                return None

            return CommandCall(prefix=prefix, args=args, rest=rest)

        return None

    def _bind(self, call: CommandCall, model: type[CommandArgs]) -> CommandArgs:
        """Разложить аргументы по полям модели и проверить."""
        positional = model.positional_fields()
        rest_name = model.rest_field()

        if rest_name is None:
            values, tail = list(call.args), None
        else:
            # Первые len(positional) слов по полям, всё остальное одной строкой.
            parts = call.rest.split(None, len(positional))
            values = parts[: len(positional)]
            tail = (
                parts[len(positional)].strip() if len(parts) > len(positional) else None
            )

        problems: list[ArgProblem] = []
        if len(values) > len(positional):
            extra = " ".join(values[len(positional) :])
            problems.append(ArgProblem("", f"лишние аргументы: {extra}", extra))
            values = values[: len(positional)]

        raw: dict[str, Any] = dict(zip(positional, values, strict=False))
        if rest_name is not None and tail is not None:
            raw[rest_name] = tail

        try:
            model_ = model.model_validate(raw)
        except ValidationError as error:
            problems += [
                ArgProblem(
                    ".".join(str(part) for part in e["loc"]),
                    _readable(e["type"], e["msg"]),
                    e.get("input"),
                )
                for e in error.errors()
            ]
        else:
            if not problems:
                return model_

        raise CommandArgsError(self.name, self.usage, tuple(problems), call.rest)

    @property
    def usage(self) -> str:
        """Как вызывать: «/calc <one> <operator: +|-|*|/> <two>»."""
        head = f"{self.prefixes[0]}{self.name}"
        return self.args_model.usage(head) if self.args_model else head

    @staticmethod
    def _is_me(ctx: BaseContext[Any], mention: str) -> bool:
        username = ctx.bot.username
        return username is not None and mention.lower() == username.lower()

    async def check(self, ctx: BaseContext[Any]) -> bool:
        call = self._parse(ctx)
        if call is None:
            return False

        if self.strict and self.args_model is not None:
            try:
                self._bind(call, self.args_model)
            except CommandArgsError:
                return False

        return True

    def call(self, ctx: BaseContext[Any]) -> CommandCall:
        """Сырой разбор: префикс, слова, остаток. Только после успешного check()."""
        call = self._parse(ctx)
        if call is None:
            raise FilterMatchError(f"{self!r} не подошёл к этому апдейту")

        return call

    def parse(self, ctx: BaseContext[Any]) -> TParsed:
        """
        Модель аргументов (или CommandCall, если модели нет). Только после успешного
        check(). Неверные аргументы: CommandArgsError.
        """
        call = self.call(ctx)
        if self.args_model is None:
            return cast(TParsed, call)

        return cast(TParsed, self._bind(call, self.args_model))

    def __repr__(self) -> str:
        return f"Command({self.name!r})"


_READABLE = {
    "missing": "не хватает аргумента",
    "int_parsing": "нужно целое число",
    "int_from_float": "нужно целое число",
    "float_parsing": "нужно число",
    "bool_parsing": "нужно да/нет (1, 0, true, false)",
    "literal_error": "недопустимое значение",
}


def _readable(kind: str, fallback: str) -> str:
    return _READABLE.get(kind, fallback)
