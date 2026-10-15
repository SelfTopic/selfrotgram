import re
from dataclasses import dataclass
from typing import Any, Generic, TypeVar, cast, overload

from pydantic import ValidationError

from ..command_args import CommandArgs
from ..context import BaseContext
from ..exceptions import ArgProblem, CommandArgsError, DefinitionError, FilterMatchError
from ..start_payload import StartPayload
from ..types import Message, TextMessage
from .base import BaseFilter, Guarantee

# Единственный алфавит, который Telegram пропускает в t.me/<bot>?start=... (см.
# start_payload.py); чтобы Command("start") без модели не забирал чужой deep link.
_DEEP_LINK_TOKEN = re.compile(r"[A-Za-z0-9_-]{1,64}")


@dataclass(frozen=True)
class CommandCall:
    """Разбор сообщения с командой."""

    prefix: str
    args: tuple[str, ...]
    rest: str  # всё после команды как написано (без крайних пробелов)


TArgs = TypeVar("TArgs", bound=CommandArgs)
TStart = TypeVar("TStart", bound=StartPayload)
# Ковариантный, чтобы AnyCommand с командами разных моделей давал `A | B`.
TParsed = TypeVar("TParsed", covariant=True)


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

    deep_link=True — у команды "start" особый смысл: параметр ссылки t.me/<bot>?
    start=..., который Telegram подставляет как весь остаток /start. Без модели —
    голый /start не заберёт чужую ссылку (ей займётся свой Command(..., deep_link=True)
    ниже или выше по списку, порядок не важен):

        start = Command("start", deep_link=True)              # не трогает /start marry_5

    С моделью StartPayload — parse(ctx) возвращает её, как обычная команда:

        class MarryLink(StartPayload, prefix="marry"):
            proposal_id: int

        marry = Command("start", MarryLink, deep_link=True)
        args = marry.parse(ctx)                                # MarryLink: proposal_id уже int
    """

    guarantees = TextMessage

    @overload
    def __init__(
        self: "Command[CommandCall]",
        name: str,
        *,
        args_count: int | None = None,
        deep_link: bool = False,
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

    @overload
    def __init__(
        self: "Command[TStart]",
        name: str,
        args: type[TStart],
        *,
        deep_link: bool,
        prefixes: str = "/",
        ignore_case: bool = False,
    ) -> None: ...

    def __init__(
        self,
        name: str,
        args: type[CommandArgs] | type[StartPayload] | None = None,
        *,
        args_count: int | None = None,
        strict: bool = False,
        deep_link: bool = False,
        prefixes: str = "/",
        ignore_case: bool = False,
    ) -> None:
        if args is not None and args_count is not None:
            raise DefinitionError(
                f"Command({name!r}): число аргументов берётся из модели, args_count не нужен"
            )

        is_start_payload = args is not None and issubclass(args, StartPayload)
        if is_start_payload and not deep_link:
            raise DefinitionError(
                f"Command({name!r}): модели StartPayload нужен deep_link=True "
                "(это deep link, не обычные аргументы команды)"
            )
        if deep_link:
            if args is not None and not is_start_payload:
                raise DefinitionError(
                    f"Command({name!r}): deep_link=True — модель аргументов должна "
                    "быть StartPayload, а не CommandArgs: deep link это один токен "
                    "без пробелов, а не слова через пробел"
                )
            if args_count is not None:
                raise DefinitionError(
                    f"Command({name!r}): deep_link=True не считает слова, "
                    "args_count не нужен"
                )
            if strict:
                raise DefinitionError(
                    f"Command({name!r}): deep_link=True и так не подходит чужому "
                    "payload, strict не нужен"
                )

        self.args_model = args
        self.deep_link = deep_link
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
        if self.args_model is None or self.deep_link:
            return head  # у StartPayload нет usage(): deep link не набирают руками

        return cast(type[CommandArgs], self.args_model).usage(head)

    @staticmethod
    def _is_me(ctx: BaseContext[Any], mention: str) -> bool:
        username = ctx.bot.username
        return username is not None and mention.lower() == username.lower()

    def matches(self, ctx: BaseContext[Any]) -> bool:
        """То же, что check(), но обычным вызовом: разбирается только строка сообщения."""
        call = self._parse(ctx)
        if call is None:
            return False

        if self.deep_link:
            return self._deep_link_matches(call.rest)

        if self.strict and self.args_model is not None:
            try:
                self._bind(call, cast(type[CommandArgs], self.args_model))
            except CommandArgsError:
                return False

        return True

    def _deep_link_matches(self, rest: str) -> bool:
        if self.args_model is None:
            # Голый /start: не забирает то, что похоже на чужой deep link — им
            # займётся Command(..., SomeStartPayload, deep_link=True), где бы он ни
            # стоял в списке хендлеров (не важен порядок, как раньше).
            return not (rest and _DEEP_LINK_TOKEN.fullmatch(rest))

        return cast(type[StartPayload], self.args_model).try_unpack(rest) is not None

    async def check(self, ctx: BaseContext[Any]) -> bool:
        return self.matches(ctx)

    def call(self, ctx: BaseContext[Any]) -> CommandCall:
        """Сырой разбор: префикс, слова, остаток. Только после успешного check()."""
        call = self._parse(ctx)
        if call is None:
            raise FilterMatchError(f"{self!r} не подошёл к этому апдейту")

        return call

    def parse(self, ctx: BaseContext[Any]) -> TParsed:
        """
        Модель аргументов (или CommandCall, если модели нет). Только после успешного
        check(). Неверные аргументы: CommandArgsError (deep_link — никогда: не
        подошедший payload уже не прошёл check()).
        """
        call = self.call(ctx)
        if self.args_model is None:
            return cast(TParsed, call)

        if self.deep_link:
            return cast(TParsed, cast(type[StartPayload], self.args_model).unpack(call.rest))

        return cast(TParsed, self._bind(call, cast(type[CommandArgs], self.args_model)))

    def __repr__(self) -> str:
        parts = [repr(self.name)]
        if self.args_model is not None:
            parts.append(self.args_model.__name__)
        if self.args_count is not None:
            parts.append(f"args_count={self.args_count}")
        if self.strict:
            parts.append("strict=True")
        if self.deep_link:
            parts.append("deep_link=True")
        if self.prefixes != ("/",):
            parts.append(f"prefixes={''.join(self.prefixes)!r}")
        if self.ignore_case:
            parts.append("ignore_case=True")
        return f"Command({', '.join(parts)})"

    def where(self, **equals: Any) -> "CommandWhere[TParsed]":
        """
        Та же команда, но срабатывает только если у разобранных аргументов указанные
        поля равны заданным значениям — ветка диспетчеризации внутри одного хендлера
        (декоратор на методе, см. handlers/base.py), не отдельный класс:

            cmd = Command("fun", FunArgs)

            class Fun(MessageHandler[BaseContext[TextMessage]]):
                @cmd.where(command=FunCommandsEnum.choice)
                async def choice(self): ...

                @cmd.where(command=FunCommandsEnum.who)
                async def who(self): ...

        Сравнение значения не трогает, какие поля заполнены — guarantee() та же, что
        у самой команды, не больше.
        """
        if self.args_model is None:
            raise DefinitionError(
                f"{self!r}.where(): нужна модель аргументов (второй параметр Command)"
            )

        unknown = set(equals) - set(self.args_model.model_fields)
        if unknown:
            raise DefinitionError(
                f"{self!r}.where(): нет полей {sorted(unknown)}; "
                f"есть {list(self.args_model.model_fields)}"
            )

        return CommandWhere(self, **equals)


class CommandWhere(BaseFilter[BaseContext[TextMessage]], Generic[TParsed]):
    """Command, у которой указанные поля разобранных аргументов равны заданным
    значениям. Создаётся через Command.where(поле=значение), не напрямую."""

    guarantees = TextMessage

    def __init__(self, cmd: "Command[TParsed]", **equals: Any) -> None:
        self.cmd = cmd
        self.equals = equals

    async def check(self, ctx: BaseContext[Any]) -> bool:
        try:
            parsed = self.cmd.parse(ctx)
        except (FilterMatchError, CommandArgsError):
            return False

        return all(getattr(parsed, name) == value for name, value in self.equals.items())

    def guarantee(self) -> Guarantee:
        return self.cmd.guarantee()

    def parse(self, ctx: BaseContext[Any]) -> TParsed:
        """Модель аргументов. Только после успешного check()."""
        return self.cmd.parse(ctx)

    def __repr__(self) -> str:
        args = ", ".join(f"{name}={value!r}" for name, value in self.equals.items())
        return f"{self.cmd!r}.where({args})"


class AnyCommand(BaseFilter[BaseContext[TextMessage]], Generic[TParsed]):
    """
    Одна команда с несколькими триггерами: у каждого своё имя, префиксы и регистр.

        transfer = AnyCommand(
            Command("transfer", TransferArgs, ignore_case=True),
            Command("перевести", TransferArgs, prefixes="", ignore_case=True),
            Command("кинуть", TransferArgs, prefixes="", ignore_case=True),
        )

        class Transfer(MessageHandler[BaseContext[TextMessage]]):
            query = transfer

            async def handle(self):
                args = transfer.parse(self.ctx)      # TransferArgs

    Подходит, если подошла любая из команд; проверяются по порядку, побеждает первая.
    parse(ctx) разбирает аргументы той команды, что сработала: неверные аргументы дают
    CommandArgsError с usage именно её. find(ctx) отдаёт саму команду, если важно знать,
    как вызвали. Модели у команд могут быть разными, тогда parse вернёт `A | B`.

    `Command("a") | Command("b")` тоже сработает как фильтр, но не скажет, какая из
    команд подошла: для parse нужна группа.
    """

    guarantees = TextMessage

    def __init__(self, *commands: Command[TParsed]) -> None:
        if not commands:
            raise DefinitionError("AnyCommand: нужна хотя бы одна команда")

        self.commands = commands

    def find(self, ctx: BaseContext[Any]) -> Command[TParsed]:
        """Первая подошедшая команда. Только после успешного check()."""
        for command in self.commands:
            if command.matches(ctx):
                return command

        raise FilterMatchError(f"{self!r} не подошёл к этому апдейту")

    async def check(self, ctx: BaseContext[Any]) -> bool:
        return any(command.matches(ctx) for command in self.commands)

    def parse(self, ctx: BaseContext[Any]) -> TParsed:
        """Модель аргументов сработавшей команды. Только после успешного check()."""
        return self.find(ctx).parse(ctx)

    def __repr__(self) -> str:
        return f"AnyCommand({', '.join(repr(command) for command in self.commands)})"


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
