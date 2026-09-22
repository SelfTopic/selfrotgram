"""
Генерирует из спецификации Bot API (github.com/PaulSonOfLars/telegram-bot-api-spec,
файл api.json):

- selfrot/types/generated.py и narrowed.py: типы и суженные типы;
- selfrot/context/accessors.py: ctx.<поле Update> для каждого поля Update;
- selfrot/handlers/kinds.py: вид обработчика для каждого поля Update;
- selfrot/filter/has.py: Has-фильтры под каждый суженный тип;
- selfrot/methods/generated.py: класс на каждый метод Bot API;
- selfrot/client/methods.py: BotMethods, методы Bot (send_message, ...);
- selfrot/context/methods.py: ярлыки на контексте (ctx.answer_message, ...).

    python scripts/generate_types.py            # из scripts/spec/telegram-bot-api.json
    python scripts/generate_types.py --fetch    # сначала скачать свежую спеку

Сгенерированное руками не правится: обновилась спека — перегенерировать.
"""

import json
import keyword
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPEC_PATH = ROOT / "scripts/spec/telegram-bot-api.json"
OUT = ROOT / "selfrot/types"
SPEC_URL = "https://raw.githubusercontent.com/PaulSonOfLars/telegram-bot-api-spec/main/api.json"

PRIMITIVES = {
    "Integer": "int",
    "String": "str",
    "Boolean": "bool",
    "Float": "float",
    "Float number": "float",
    "True": "bool",
}
RESERVED = {
    "Optional",
    "List",
    "Union",
    "Literal",
    "Annotated",
    "Field",
    "BaseModel",
    "ConfigDict",
}
# Типы, у которых своё определение (загружаемый файл, а не JSON-объект).
HAND_WRITTEN_TYPES = {"InputFile"}
# «always “user”» (в кавычках) и «must be photo» (без них: InputMedia*, InlineQueryResult*).
DISCRIMINATOR = re.compile(
    r"(?:always|must be)\s+(?:[“\"]([^”\"]+)[”\"]|([A-Za-z][A-Za-z0-9_]*))"
)
PREFERRED_DISCRIMINATORS = ("type", "status", "source")


def load_spec() -> dict:
    if "--fetch" in sys.argv:
        SPEC_PATH.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(SPEC_URL, timeout=60) as response:
            SPEC_PATH.write_bytes(response.read())
    return json.loads(SPEC_PATH.read_text(encoding="utf-8"))


def py_type(types: list[str]) -> str:
    def one(name: str) -> str:
        depth = 0
        while name.startswith("Array of "):
            name = name[len("Array of ") :]
            depth += 1

        result = PRIMITIVES.get(name, name)
        for _ in range(depth):
            result = f"List[{result}]"
        return result

    parts = [one(t) for t in types]
    return parts[0] if len(parts) == 1 else f"Union[{', '.join(parts)}]"


def attr_name(name: str) -> tuple[str, str | None]:
    """(имя атрибута, alias). from -> user (так называется поле в selfrot)."""
    if name == "from":
        return "user", "from"
    if keyword.iskeyword(name):
        return name + "_", name
    return name, None


def pascal(name: str) -> str:
    return "".join(part.capitalize() for part in name.split("_"))


def docstring(text: str, indent: str) -> str:
    text = text.replace("\\", "\\\\").replace('"""', '\\"\\"\\"').strip()
    if text.endswith('"'):
        text += " "
    lines = text.split("\n")
    body = ("\n" + indent).join(lines)
    return (
        f'{indent}"""{body}"""'
        if len(lines) == 1
        else f'{indent}"""{body}\n{indent}"""'
    )


def find_discriminator(
    types: dict, subtypes: list[str]
) -> tuple[str, dict[str, str]] | None:
    """Поле, по которому Telegram различает подтипы (`always “user”`), у всех."""
    if any(sub not in types for sub in subtypes):
        return None

    per_subtype: dict[str, dict[str, str]] = {}
    for sub in subtypes:
        found = {}
        for field in types[sub].get("fields", []):
            match = DISCRIMINATOR.search(field["description"])
            if match and field["types"] == ["String"]:
                found[field["name"]] = match.group(1) or match.group(2)
        per_subtype[sub] = found

    common = (
        set.intersection(*(set(v) for v in per_subtype.values()))
        if per_subtype
        else set()
    )
    if not common:
        return None

    name = next((n for n in PREFERRED_DISCRIMINATORS if n in common), sorted(common)[0])
    values = {sub: found[name] for sub, found in per_subtype.items()}
    if len(set(values.values())) != len(values):
        return None
    return name, values


def check_names(types: dict) -> None:
    from pydantic import BaseModel

    base_attrs = set(dir(BaseModel))
    for name, t in types.items():
        assert name not in RESERVED, f"имя типа {name} конфликтует с импортами"
        for field in t.get("fields", []):
            assert not any("InputFile" in x for x in field["types"]), (
                f"{name}.{field['name']}: InputFile в поле типа — pydantic-модели "
                "не умеют его хранить, нужен отдельный разбор"
            )
        for field in t.get("fields", []):
            attr, _ = attr_name(field["name"])
            assert attr not in base_attrs, (
                f"{name}.{attr}: конфликт с атрибутом BaseModel"
            )


def narrowed_types(types: dict) -> list[tuple[str, str, str, dict]]:
    """(класс, корневой тип, атрибут, поле) для каждого суженного типа."""
    roots = ["Message"]
    for field in types["Update"]["fields"]:
        root = field["types"][0]
        if field["name"] != "update_id" and root not in roots:
            roots.append(root)

    result: list[tuple[str, str, str, dict]] = []
    seen: set[str] = set()
    for root in roots:
        for field in types[root].get("fields", []):
            if field["required"]:
                continue

            attr, _ = attr_name(field["name"])
            cls = f"{pascal(attr)}{root}"
            assert cls not in types, f"{cls} совпадает с типом Bot API"
            assert cls not in seen, f"{cls} сгенерирован дважды"
            seen.add(cls)
            result.append((cls, root, attr, field))

    return result


# Условия над ответом (reply_to_message), для которых есть готовые Reply[...] и HasReply*.
# Любое другое условие: свой Reply[...] и свой фильтр (docs/design.md).
# Только то, что нужно часто; остальное (опросы, локации и т. п.) это узкая логика, для неё
# хватает if в хендлере. У самого ответа reply_to_message Telegram не заполняет, так что глубже
# одного уровня вложенности не бывает.
REPLY_ATTRS = (
    "user",
    "text",
    "entities",
    "caption",
    "caption_entities",
    "photo",
    "animation",
    "audio",
    "document",
    "sticker",
    "video",
    "video_note",
    "voice",
)


def reply_types(types: dict) -> list[tuple[str, str, str, str]]:
    """(алиас, внутренний тип, атрибут, фильтр): ReplyUserMessage, UserMessage, user, HasReplyUser."""
    inner = {a: c for c, root, a, _ in narrowed_types(types) if root == "Message"}
    taken = {c for c, *_ in narrowed_types(types)} | {"Reply"}
    result = []
    for attr in REPLY_ATTRS:
        assert attr in inner, f"REPLY_ATTRS: у Message нет необязательного поля {attr}"
        alias = f"Reply{inner[attr]}"
        assert alias not in types and alias not in taken, f"{alias} уже занят"
        result.append((alias, inner[attr], attr, f"HasReply{pascal(attr)}"))

    assert "Reply" not in types, "Reply совпадает с типом Bot API"
    return result


def generate(spec: dict) -> tuple[str, str]:
    types: dict = spec["types"]
    check_names(types)
    version = f"{spec['version']}, {spec['release_date']}"

    unions = {n: t["subtypes"] for n, t in types.items() if t.get("subtypes")}
    discriminators = {n: find_discriminator(types, subs) for n, subs in unions.items()}

    def refers_to_itself(name: str, subs: list[str]) -> bool:
        return any(name in py_type([sub]) for sub in subs if sub not in types)

    recursive = {n for n, subs in unions.items() if refers_to_itself(n, subs)}

    # Литерал по умолчанию — у каждого типа отдельно, независимо от того, удалось ли
    # собрать дискриминатор для всего объединения (у InlineQueryResultPhoto и
    # InlineQueryResultCachedPhoto одинаковое «photo», а обязательный type: str без
    # значения заставлял бы писать его руками).
    literals: dict[tuple[str, str], str] = {}
    for type_name, t in types.items():
        for field in t.get("fields", []):
            if (
                field["required"]
                and field["name"] in PREFERRED_DISCRIMINATORS
                and field["types"] == ["String"]
            ):
                match = DISCRIMINATOR.search(field["description"])
                if match:
                    literals[(type_name, field["name"])] = match.group(1) or match.group(2)

    out = [
        f"# АВТОГЕНЕРАЦИЯ: scripts/generate_types.py, Telegram {version}.",
        "# Руками не править — обновилась спека, перегенерировать.",
        "# ruff: noqa",
        "from __future__ import annotations",
        "",
        "from typing import TYPE_CHECKING, Annotated, Any, List, Literal, Optional, Union",
        "",
        "from pydantic import BaseModel, ConfigDict, Discriminator, Field, PrivateAttr, Tag",
        "from typing_extensions import TypeAliasType",
        "",
        "from ..exceptions import BotNotBoundError",
        "from .input_file import InputFile",
        "",
        "if TYPE_CHECKING:",
        "    from ..client.methods import BotMethods",
        "",
        "",
        "class _Base(BaseModel, frozen=True):",
        "    # protected_namespaces=(): в Bot API есть поле model_custom_emoji_id.",
        "    model_config = ConfigDict(populate_by_name=True, protected_namespaces=())",
        "",
        "    # Бот, с которым объект получен (Bot.call и вебхук передают его в контексте",
        "    # валидации). Нужен методам на объектах: message.answer(...), callback.answer().",
        "    _bot: Any = PrivateAttr(default=None)",
        "",
        "    def model_post_init(self, context: Any, /) -> None:",
        "        # Модель frozen, поэтому не self._bot = ..., а напрямую в приватное хранилище.",
        "        private = self.__pydantic_private__",
        "        if private is not None and isinstance(context, dict):",
        "            if context.get(\"bot\") is not None:",
        "                private[\"_bot\"] = context[\"bot\"]",
        "",
        "    def _require_bot(self) -> BotMethods:",
        "        if self._bot is None:",
        "            raise BotNotBoundError(",
        "                f\"{type(self).__name__} не привязан к боту: объект создан вручную или \"",
        "                \"разобран без контекста {'bot': ...}. Вызовите метод у бота напрямую\"",
        "            )",
        "        return self._bot",
        "",
    ]

    # Рекурсивное объединение (RichText) обязано стоять до классов, которые его
    # используют, иначе pyright отвергает ссылку на самого себя; члены — в кавычках.
    for name in sorted(recursive):
        members = ", ".join(
            py_type([sub]) if sub not in types else f'"{sub}"' for sub in unions[name]
        )
        members = members.replace(f"List[{name}]", f'List["{name}"]')
        out += ["", f'{name} = TypeAliasType("{name}", Union[{members}])']

    bound = bound_methods(spec)

    for name, t in types.items():
        if name in unions or name in HAND_WRITTEN_TYPES:
            continue

        out += ["", f"class {name}(_Base, frozen=True):"]
        paragraphs = t.get("description") or []
        doc = (
            "\n\n".join([*paragraphs, t["href"]])
            if isinstance(paragraphs, list)
            else str(paragraphs)
        )
        out.append(docstring(doc, "    "))

        for field in t.get("fields", []):
            attr, alias = attr_name(field["name"])
            literal = literals.get((name, field["name"]))
            annotation = f'Literal["{literal}"]' if literal else py_type(field["types"])

            if field["required"]:
                if literal:
                    # Значение единственное, поэтому при создании объекта его не пишут:
                    # InputMediaPhoto(media="id"), а не InputMediaPhoto(type="photo", ...).
                    default = f" = Field(default={literal!r})"
                else:
                    default = f" = Field(alias={alias!r})" if alias else ""
                out.append(f"    {attr}: {annotation}{default}")
            else:
                args = "default=None" + (f", alias={alias!r}" if alias else "")
                out.append(f"    {attr}: Optional[{annotation}] = Field({args})")

            out.append(docstring(field["description"], "    "))

        for item in bound.get(name, []):
            out += render_bound_method(item, spec)

    out += ["", ""]
    for name, subs in unions.items():
        if name in recursive:
            continue

        members = ", ".join(py_type([sub]) for sub in subs)
        found = discriminators[name]
        if found:
            out.append(
                f"{name} = Annotated[Union[{members}], "
                f'Field(discriminator="{found[0]}")]'
            )
        elif name == "MaybeInaccessibleMessage":
            # У InaccessibleMessage те же поля, что у Message (chat, message_id, date),
            # поэтому без правила разбор всегда выбирал бы Message. Отличает их date == 0.
            out += [
                "def _maybe_inaccessible_tag(value: Any) -> str:",
                '    date = value.get("date") if isinstance(value, dict) else getattr(value, "date", None)',
                '    return "inaccessible" if date == 0 else "message"',
                "",
                f"{name} = Annotated[",
                "    Union[",
                '        Annotated[Message, Tag("message")],',
                '        Annotated[InaccessibleMessage, Tag("inaccessible")],',
                "    ],",
                "    Discriminator(_maybe_inaccessible_tag),",
                "]",
            ]
        else:
            out.append(f"{name} = Union[{members}]")

    names = [n for n in types if n not in HAND_WRITTEN_TYPES]
    out += [
        "",
        "",
        "__all__ = [",
        *[f'    "{n}",' for n in names],
        "]",
        "",
        "for _name in __all__:",
        "    _model = globals()[_name]",
        "    if isinstance(_model, type):",
        "        _model.model_rebuild()",
        "",
    ]
    generated = "\n".join(out)

    narrowed = [
        f"# АВТОГЕНЕРАЦИЯ: scripts/generate_types.py, Telegram {version}.",
        "# Руками не править — обновилась спека, перегенерировать.",
        "# ruff: noqa",
        "# Суженный тип переопределяет поле без значения по умолчанию",
        "# (в рантайме он не создаётся, сужение типа при этом работает). Новые",
        "# Pylance ругаются на каждое такое поле, поэтому правило выключено",
        "# только в этом файле.",
        "# pyright: reportGeneralTypeIssues=false",
        '"""',
        "Тип с гарантированно заполненным полем: <Поле><Тип> (TextMessage,",
        "DataCallbackQuery). Такие типы есть для Message и для каждого объекта,",
        "который Bot API кладёт в Update. Нужны для сужения типа (cast), в",
        "рантайме отдельно не создаются. Комбинация гарантий одного типа —",
        "наследование: class PhotoCaption(PhotoMessage, CaptionMessage, frozen=True).",
        "",
        "Условие над ответом: Reply[<суженный тип ответа>], например Reply[UserMessage]",
        "(ниже готовые алиасы ReplyUserMessage и другие). Условия над ответом тоже",
        "складываются наследованием, но внутреннего типа: Reply[PhotoCaption].",
        '"""',
        "from __future__ import annotations",
        "",
        "from typing import Generic, List, Literal, TypeVar, Union",
        "",
        "from pydantic import ConfigDict, Field",
        "",
        "from .generated import *",
        "",
        "",
        'TReply = TypeVar("TReply", bound=Message)',
        "",
        "",
        "class Reply(Message, Generic[TReply], frozen=True):",
        '    """Message, у которого гарантированно есть `reply_to_message` суженного типа."""',
        "",
        "    # Только для cast: в рантайме не создаётся, сборка отложена.",
        "    model_config = ConfigDict(defer_build=True)",
        "    reply_to_message: TReply = Field()",
    ]

    narrowed_names = []
    for cls, root, attr, field in narrowed_types(types):
        _, alias = attr_name(field["name"])
        narrowed_names.append(cls)

        args = f"alias={alias!r}" if alias else ""
        narrowed += [
            "",
            "",
            f"class {cls}({root}, frozen=True):",
            f'    """{root}, у которого гарантированно есть `{attr}`."""',
            "",
            "    # Только для cast: в рантайме не создаются, сборка отложена.",
            "    model_config = ConfigDict(defer_build=True)",
            f"    {attr}: {py_type(field['types'])} = Field({args})",
        ]

    replies = reply_types(types)
    narrowed += ["", "", "# Готовые условия над ответом: Reply[<суженный тип>]."]
    narrowed += [f"{alias} = Reply[{inner}]" for alias, inner, _, _ in replies]

    narrowed += [
        "",
        "",
        "__all__ = [",
        '    "Reply",',
        *[f'    "{a}",' for a, *_ in replies],
        *[f'    "{n}",' for n in narrowed_names],
        "]",
        "",
    ]
    return generated, "\n".join(narrowed)


def update_fields(types: dict) -> list[tuple[str, str]]:
    """(поле Update, корневой тип) в порядке спецификации, без update_id."""
    return [
        (field["name"], field["types"][0])
        for field in types["Update"]["fields"]
        if field["name"] != "update_id"
    ]


def generate_accessors(spec: dict) -> str:
    types = spec["types"]
    fields = update_fields(types)
    roots = list(dict.fromkeys(root for _, root in fields))
    version = f"{spec['version']}, {spec['release_date']}"

    out = [
        f"# АВТОГЕНЕРАЦИЯ: scripts/generate_types.py, Telegram {version}.",
        "# Руками не править — обновилась спека, перегенерировать.",
        "# ruff: noqa",
        "from __future__ import annotations",
        "",
        "from typing import Generic, Optional, Union, cast",
        "",
        "from typing_extensions import TypeVar",
        "",
        "from ..types import (",
        "    Message,",
        *[f"    {root}," for root in roots if root != "Message"],
        "    Update,",
        ")",
        "",
        "Event = Union[" + ", ".join(roots) + "]",
        "",
        "# Что обещает заголовок хендлера: AppContext[TextMessage],",
        "# AppContext[DataCallbackQuery].",
        "# По умолчанию — как раньше: сообщение, которое может отсутствовать.",
        'TEvent = TypeVar("TEvent", covariant=True, default=Optional[Message])',
        "",
    ]
    for root in roots:
        out.append(f'_T{root} = TypeVar("_T{root}", bound=Optional[{root}])')

    out += [
        "",
        "_EVENT_FIELDS = (",
        *[f'    "{name}",' for name, _ in fields],
        ")",
        "",
        "",
        "class EventAccessors(Generic[TEvent]):",
        '    """',
        "    ctx.<поле Update> для каждого поля Update. Доступ типизирован через self:",
        "    AppContext[TextMessage] даёт ctx.message: TextMessage, а",
        "    ctx.callback_query",
        "    в нём — ошибка типов. Без параметра — ctx.message: Optional[Message].",
        "    Ограничение: message/edited_message/... делят один корневой тип, поэтому",
        "    тип не отличает их между собой — берите поле своего вида обработчика.",
        '    """',
        "",
        "    update: Update",
        "",
        "    @property",
        "    def event(self) -> Optional[Event]:",
        '        """Объект апдейта: заполнено не больше одного поля Update."""',
        "        for name in _EVENT_FIELDS:",
        "            value = getattr(self.update, name)",
        "            if value is not None:",
        "                return value",
        "",
        "        return None",
    ]
    for name, root in fields:
        out += [
            "",
            "    @property",
            f"    def {name}(self: EventAccessors[_T{root}]) -> _T{root}:",
            f"        return cast(_T{root}, self.update.{name})",
        ]

    out += [
        "",
        "",
        '__all__ = ["Event", "EventAccessors", "TEvent"]',
        "",
    ]
    return "\n".join(out)


def generate_kinds(spec: dict) -> str:
    types = spec["types"]
    fields = update_fields(types)
    roots = list(dict.fromkeys(root for _, root in fields))
    version = f"{spec['version']}, {spec['release_date']}"

    out = [
        f"# АВТОГЕНЕРАЦИЯ: scripts/generate_types.py, Telegram {version}.",
        "# Руками не править — обновилась спека, перегенерировать.",
        "# ruff: noqa",
        "from __future__ import annotations",
        "",
        "from typing import ClassVar",
        "",
        "from pydantic import BaseModel",
        "",
        "from ..context import TContext",
        "from ..types import (",
        *[f"    {root}," for root in roots],
        ")",
        "from .base import BaseHandler",
    ]
    names = []
    for name, root in fields:
        cls = f"{pascal(name)}Handler"
        names.append(cls)
        out += [
            "",
            "",
            f"class {cls}(BaseHandler[TContext]):",
            f'    """Апдейты с полем `{name}` ({root})."""',
            "",
            f'    update_field: ClassVar[str] = "{name}"',
            f"    payload_type: ClassVar[type[BaseModel]] = {root}",
        ]

    out += ["", "", "__all__ = [", *[f'    "{n}",' for n in names], "]", ""]
    return "\n".join(out)


def has_filter_name(cls: str, root: str, attr: str) -> str:
    """Message — частый корень: HasText. Остальные с типом: HasDataCallbackQuery."""
    return f"Has{pascal(attr)}" if root == "Message" else f"Has{cls}"


def generate_has_filters(spec: dict) -> str:
    version = f"{spec['version']}, {spec['release_date']}"
    out = [
        f"# АВТОГЕНЕРАЦИЯ: scripts/generate_types.py, Telegram {version}.",
        "# Руками не править — обновилась спека, перегенерировать.",
        "# ruff: noqa",
        '"""',
        "Фильтры «у объекта апдейта заполнено поле»: по одному на каждый суженный тип.",
        "HasText гарантирует TextMessage, HasDataCallbackQuery — DataCallbackQuery.",
        '"""',
        "from __future__ import annotations",
        "",
        "from typing import Any",
        "",
        "from ..context import BaseContext",
        "from ..types import *",
        "from .base import BaseFilter",
    ]
    names: list[str] = []
    for cls, root, attr, _ in narrowed_types(spec["types"]):
        name = has_filter_name(cls, root, attr)
        assert name not in names, f"фильтр {name} сгенерирован дважды"
        names.append(name)
        out += [
            "",
            "",
            f"class {name}(BaseFilter[BaseContext[{cls}]]):",
            f'    """У объекта {root} заполнено `{attr}`. Гарантирует {cls}."""',
            "",
            f"    guarantees = {cls}",
            "",
            "    async def check(self, ctx: BaseContext[Any]) -> bool:",
            "        event = ctx.event",
            f"        return isinstance(event, {root}) and event.{attr} is not None",
        ]

    for alias, inner, attr, name in reply_types(spec["types"]):
        assert name not in names, f"фильтр {name} сгенерирован дважды"
        names.append(name)
        out += [
            "",
            "",
            f"class {name}(BaseFilter[BaseContext[{alias}]]):",
            f'    """У ответа `reply_to_message` заполнено `{attr}`. Гарантирует {alias}."""',
            "",
            f"    guarantees = {alias}",
            "",
            "    async def check(self, ctx: BaseContext[Any]) -> bool:",
            "        event = ctx.event",
            "        reply = event.reply_to_message if isinstance(event, Message) else None",
            f"        return reply is not None and reply.{attr} is not None",
        ]

    out += ["", "", "__all__ = [", *[f'    "{n}",' for n in sorted(names)], "]", ""]
    return "\n".join(out)


def snake(name: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


def collapse(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def check_method_names(spec: dict) -> None:
    types = spec["types"]
    reserved = {"data", "to_payload"}
    seen: set[str] = set()
    for name, method in spec["methods"].items():
        cls = name[0].upper() + name[1:]
        assert cls not in types, f"метод {name}: класс {cls} совпадает с типом Bot API"
        assert snake(name) not in seen, f"метод {name}: snake_case-имя занято"
        seen.add(snake(name))
        for field in method.get("fields", []):
            assert field["name"] not in reserved, (
                f"{name}.{field['name']} зарезервировано"
            )
            assert not keyword.iskeyword(field["name"]), (
                f"{name}.{field['name']}: ключевое слово"
            )


def generate_methods(spec: dict) -> str:
    version = f"{spec['version']}, {spec['release_date']}"
    out = [
        f"# АВТОГЕНЕРАЦИЯ: scripts/generate_types.py, Telegram {version}.",
        "# Руками не править — обновилась спека, перегенерировать.",
        "# ruff: noqa",
        "from __future__ import annotations",
        "",
        "from dataclasses import dataclass",
        "from typing import Any, ClassVar, List, Optional, Union",
        "",
        "from ..types import *",
        "from .base import TelegramMethod",
    ]
    names = []
    for name, method in spec["methods"].items():
        cls = name[0].upper() + name[1:]
        names.append(cls)
        doc = "\n\n".join([*method["description"], method["href"]])
        out += [
            "",
            "",
            "@dataclass(kw_only=True)",
            f"class {cls}(TelegramMethod[{py_type(method['returns'])}]):",
            docstring(doc, "    "),
            "",
            f'    __api_method__: ClassVar[str] = "{name}"',
            f"    __returning__: ClassVar[Any] = {py_type(method['returns'])}",
        ]
        for field in method.get("fields", []):
            annotation = py_type(field["types"])
            if field["required"]:
                out.append(f"    {field['name']}: {annotation}")
            else:
                out.append(f"    {field['name']}: Optional[{annotation}] = None")

            out.append(docstring(field["description"], "    "))

    out += ["", "", "__all__ = [", *[f'    "{n}",' for n in names], "]", ""]
    return "\n".join(out)


def generate_bot_methods(spec: dict) -> str:
    version = f"{spec['version']}, {spec['release_date']}"
    out = [
        f"# АВТОГЕНЕРАЦИЯ: scripts/generate_types.py, Telegram {version}.",
        "# Руками не править — обновилась спека, перегенерировать.",
        "# ruff: noqa",
        "from __future__ import annotations",
        "",
        "from typing import List, Optional, TypeVar, Union",
        "",
        "from ..methods import *",
        "from ..methods.base import TelegramMethod",
        "from ..types import *",
        "",
        'T = TypeVar("T")',
        "",
        "",
        "class BotMethods:",
        '    """Все методы Bot API. Не хватает только call(): его даёт Bot."""',
        "",
        "    async def call(self, method: TelegramMethod[T]) -> T:",
        "        raise NotImplementedError",
    ]
    for name, method in spec["methods"].items():
        cls = name[0].upper() + name[1:]
        fields = method.get("fields", [])
        required = [f for f in fields if f["required"]]
        optional = [f for f in fields if not f["required"]]

        params = ["self"]
        for field in required:
            params.append(f"{field['name']}: {py_type(field['types'])}")
        if optional:
            params.append("*")
            for field in optional:
                params.append(
                    f"{field['name']}: Optional[{py_type(field['types'])}] = None"
                )

        doc = "\n\n".join([*method["description"], method["href"]])
        if fields:
            doc += "\n\nArgs:\n" + "\n".join(
                f"    {f['name']}: {collapse(f['description'])}" for f in fields
            )

        out += [
            "",
            f"    async def {snake(name)}(",
            *[f"        {p}," for p in params],
            f"    ) -> {py_type(method['returns'])}:",
            docstring(doc, "        "),
            f"        return await self.call({cls}(",
            *[f"            {f['name']}={f['name']}," for f in fields],
            "        ))",
        ]

    out.append("")
    return "\n".join(out)


def context_shortcuts(spec: dict) -> list[dict]:
    """Какие методы Bot получают ярлык на контексте и как подставляются аргументы."""
    types, methods = spec["types"], spec["methods"]
    roots = dict(update_fields(types))
    shortcuts: list[dict] = []

    for name, method in methods.items():
        fields = {f["name"]: f for f in method.get("fields", [])}
        chat_required = "chat_id" in fields and fields["chat_id"]["required"]
        stem = snake(name)

        if name.startswith("send") and chat_required:
            suffix = stem[len("send_") :]
            shortcuts.append(
                {"ctx": f"answer_{suffix}", "method": name, "kind": "answer"}
            )
            if "reply_parameters" in fields:
                shortcuts.append(
                    {"ctx": f"reply_{suffix}", "method": name, "kind": "reply"}
                )
        elif name.startswith("answer") and name.endswith("Query"):
            event = stem[len("answer_") :]
            if event in roots and f"{event}_id" in fields:
                shortcuts.append(
                    {"ctx": stem, "method": name, "kind": "query", "event": event}
                )
        elif {"chat_id", "message_id", "inline_message_id"} <= set(fields):
            shortcuts.append({"ctx": stem, "method": name, "kind": "target"})
        elif "from_chat_id" in fields and chat_required:
            shortcuts.append({"ctx": stem, "method": name, "kind": "forward"})
        elif chat_required:
            shortcuts.append({"ctx": stem, "method": name, "kind": "chat"})

    return shortcuts


# В спеке это поле необязательное (текст или rich_message), но основное: его пишут
# первым аргументом, msg.edit_text("готово"), а не msg.edit_text(text="готово").
POSITIONAL_FIRST = {
    "editMessageText": "text",
    "editMessageCaption": "caption",
    "answerCallbackQuery": "text",
}


def split_params(method_name: str, fields: list[dict]) -> tuple[list[dict], list[dict], dict | None]:
    """(обязательные, необязательные, основное поле, ставшее позиционным)."""
    first = POSITIONAL_FIRST.get(method_name)
    promoted = next((f for f in fields if f["name"] == first), None) if first else None
    required = [f for f in fields if f["required"]]
    optional = [f for f in fields if not f["required"] and f is not promoted]
    return required, optional, promoted


# Как называются на объекте методы, у которых обычное имя не подходит.
BOUND_RENAMES = {"copy_message": "copy_to", "read_business_message": "read"}


def bound_name(stem: str) -> str:
    """delete_message -> delete, edit_message_text -> edit_text, pin_chat_message -> pin."""
    if stem in BOUND_RENAMES:
        return BOUND_RENAMES[stem]
    return stem.replace("_chat_message", "").replace("_message", "")


def bound_methods(spec: dict) -> dict[str, list[dict]]:
    """
    Методы Bot API, которые вызываются на самом объекте (тип -> список):
    message.answer/reply/edit_text/delete/pin/forward, callback.answer(),
    inline_query.answer(), chat_member_updated.answer().
    """
    types, methods = spec["types"], spec["methods"]
    roots = dict(update_fields(types))
    result: dict[str, list[dict]] = {"Message": [], "ChatMemberUpdated": []}

    for name, method in methods.items():
        fields = {f["name"]: f for f in method.get("fields", [])}
        chat_required = "chat_id" in fields and fields["chat_id"]["required"]
        stem = snake(name)

        if name.startswith("send") and chat_required:
            suffix = stem[len("send_") :]
            tail = "" if suffix == "message" else f"_{suffix}"
            result["Message"].append(
                {"name": f"answer{tail}", "method": name, "kind": "answer"}
            )
            if "reply_parameters" in fields:
                result["Message"].append(
                    {"name": f"reply{tail}", "method": name, "kind": "reply"}
                )
            result["ChatMemberUpdated"].append(
                {"name": f"answer{tail}", "method": name, "kind": "chat_answer"}
            )
        elif name.startswith("answer") and name.endswith("Query"):
            event = stem[len("answer_") :]
            if event in roots and f"{event}_id" in fields:
                result.setdefault(roots[event], []).append(
                    {
                        "name": "answer",
                        "method": name,
                        "kind": "query",
                        "id_field": f"{event}_id",
                    }
                )
        elif "from_chat_id" in fields and chat_required and "message_id" in fields:
            result["Message"].append(
                {"name": bound_name(stem), "method": name, "kind": "forward"}
            )
        elif "chat_id" in fields and "message_id" in fields:
            result["Message"].append(
                {"name": bound_name(stem), "method": name, "kind": "own"}
            )

    for type_name, items in result.items():
        own_fields = {f["name"] for f in types[type_name].get("fields", [])}
        names = [item["name"] for item in items]
        assert len(names) == len(set(names)), f"{type_name}: имена методов повторяются"
        assert not set(names) & own_fields, f"{type_name}: имя метода совпало с полем"

    return result


BOUND_NOTES = {
    "answer": "чат — чат этого сообщения",
    "reply": "чат — чат этого сообщения, цитирует его",
    "chat_answer": "чат — чат этого события",
    "query": "id запроса берётся из объекта",
    "forward": "источник — это сообщение, чат назначения задаёте вы",
    "own": "правит это сообщение",
}


def render_bound_method(item: dict, spec: dict) -> list[str]:
    method = spec["methods"][item["method"]]
    kind = item["kind"]
    fields = method.get("fields", [])
    by_name = {f["name"]: f for f in fields}

    dropped: dict[str, str] = {}  # поле -> выражение, которым оно заполняется
    omitted: set[str] = set()  # поля, которые не передаём вообще
    if kind in ("answer", "reply", "chat_answer", "own"):
        dropped["chat_id"] = "self.chat.id"
    if kind == "forward":
        dropped["from_chat_id"] = "self.chat.id"
    if kind in ("forward", "own"):
        dropped["message_id"] = "self.message_id"
    if kind == "own":
        omitted.add("inline_message_id")
    if kind == "query":
        dropped[item["id_field"]] = "self.id"

    exposed = [f for f in fields if f["name"] not in dropped | dict.fromkeys(omitted)]
    required, optional, promoted = split_params(item["method"], exposed)
    params = ["self"] + [f"{f['name']}: {py_type(f['types'])}" for f in required]
    if promoted:
        params.append(f"{promoted['name']}: Optional[{py_type(promoted['types'])}] = None")
    if optional:
        params.append("*")
        params += [f"{f['name']}: Optional[{py_type(f['types'])}] = None" for f in optional]

    def expression(name: str) -> str | None:
        if name in dropped:
            return dropped[name]
        if name in omitted:
            return None
        if kind in ("answer", "reply") and name == "business_connection_id":
            return (
                "business_connection_id if business_connection_id is not None "
                "else self.business_connection_id"
            )
        if kind in ("answer", "reply") and name == "message_thread_id":
            return (
                "message_thread_id if message_thread_id is not None else "
                "(self.message_thread_id if self.is_topic_message else None)"
            )
        if kind == "reply" and name == "reply_parameters":
            return (
                "reply_parameters if reply_parameters is not None "
                "else ReplyParameters(message_id=self.message_id)"
            )
        return name

    doc = f"Как bot.{snake(item['method'])}(), но {BOUND_NOTES[kind]}."
    doc += "\n\n" + "\n\n".join([*method["description"], method["href"]])
    lines = [
        "",
        f"    async def {item['name']}(",
        *[f"        {p}," for p in params],
        f"    ) -> {py_type(method['returns'])}:",
        docstring(doc, "        "),
        f"        return await self._require_bot().{snake(item['method'])}(",
    ]
    for f in fields:
        value = expression(f["name"])
        if value is not None:
            lines.append(f"            {f['name']}={value},")
    lines.append("        )")
    assert set(by_name) >= dropped.keys(), item
    return lines


CONTEXT_NOTES = {
    "answer": "чат берётся из апдейта",
    "reply": "чат берётся из апдейта, сообщение цитирует сообщение апдейта",
    "query": "id запроса берётся из апдейта",
    "target": "правит сообщение апдейта (или inline-сообщение), если цель не задана",
    "chat": "chat_id берётся из апдейта",
    "forward": "from_chat_id и message_id берутся из апдейта",
}


def generate_context_methods(spec: dict) -> str:
    types, methods = spec["types"], spec["methods"]
    version = f"{spec['version']}, {spec['release_date']}"
    roots = dict(update_fields(types))
    shortcuts = context_shortcuts(spec)

    taken = {"update", "bot", "event", "chat", "chat_id", "user", "message_id", *roots}
    seen: set[str] = set()
    for item in shortcuts:
        assert item["ctx"] not in taken | seen, f"ярлык {item['ctx']} уже занят"
        seen.add(item["ctx"])

    query_roots = sorted(
        {roots[item["event"]] for item in shortcuts if item["kind"] == "query"}
    )
    out = [
        f"# АВТОГЕНЕРАЦИЯ: scripts/generate_types.py, Telegram {version}.",
        "# Руками не править — обновилась спека, перегенерировать.",
        "# ruff: noqa",
        "from __future__ import annotations",
        "",
        "from typing import List, Optional, Union",
        "",
        "from ..types import *",
        "from .accessors import TEvent, " + ", ".join(f"_T{r}" for r in query_roots),
        "from .helpers import ContextHelpers",
        "",
        "",
        "class ContextMethods(ContextHelpers[TEvent]):",
        '    """',
        "    Ярлыки методов Bot: то же, что bot.<метод>(...), но чат, сообщение и id",
        "    запроса берутся из текущего апдейта. answer_* пишет в чат, reply_* ещё и",
        "    цитирует сообщение. Для другого чата: ctx.bot.<метод>(...).",
        '    """',
    ]

    for item in shortcuts:
        method = methods[item["method"]]
        kind = item["kind"]
        fields = method.get("fields", [])
        by_name = {f["name"]: f for f in fields}

        dropped: set[str] = set()
        made_optional: set[str] = set()
        if kind in ("answer", "reply", "chat"):
            dropped.add("chat_id")
        if kind == "forward":
            dropped.add("from_chat_id")
        if kind == "query":
            dropped.add(f"{item['event']}_id")
        if (
            kind in ("chat", "forward")
            and "message_id" in by_name
            and by_name["message_id"]["required"]
        ):
            made_optional.add("message_id")

        exposed = [f for f in fields if f["name"] not in dropped]
        required = [
            f for f in exposed if f["required"] and f["name"] not in made_optional
        ]
        optional = [
            f for f in exposed if not f["required"] or f["name"] in made_optional
        ]
        first = POSITIONAL_FIRST.get(item["method"])
        promoted = next((f for f in optional if f["name"] == first), None)
        optional = [f for f in optional if f is not promoted]

        self_arg = "self"
        if kind == "query":
            self_arg = f"self: ContextMethods[_T{roots[item['event']]}]"

        params = [self_arg] + [f"{f['name']}: {py_type(f['types'])}" for f in required]
        if promoted:
            params.append(
                f"{promoted['name']}: Optional[{py_type(promoted['types'])}] = None"
            )
        if optional:
            params.append("*")
            params += [
                f"{f['name']}: Optional[{py_type(f['types'])}] = None" for f in optional
            ]

        def expression(field: dict) -> str:
            n = field["name"]
            if n in ("chat_id", "from_chat_id") and n in dropped:
                return "self.chat_id"
            if kind == "query" and n in dropped:
                return f'self._event_id("{item["event"]}")'
            if kind in ("answer", "reply") and n in (
                "business_connection_id",
                "message_thread_id",
            ):
                return f'self._or_default("{n}", {n})'
            if kind == "reply" and n == "reply_parameters":
                return (
                    "reply_parameters if reply_parameters is not None "
                    "else self._reply_parameters()"
                )
            if n in made_optional:
                return (
                    "message_id if message_id is not None "
                    "else self._require_message_id()"
                )
            return n

        doc = f"Как bot.{snake(item['method'])}(), но {CONTEXT_NOTES[kind]}."
        doc += "\n\n" + "\n\n".join([*method["description"], method["href"]])
        if exposed:
            doc += "\n\nArgs:\n" + "\n".join(
                f"    {f['name']}: {collapse(f['description'])}" for f in exposed
            )

        out += [
            "",
            f"    async def {item['ctx']}(",
            *[f"        {p}," for p in params],
            f"    ) -> {py_type(method['returns'])}:",
            docstring(doc, "        "),
        ]
        if kind == "target":
            out.append(
                "        chat_id, message_id, inline_message_id = "
                "self._message_target(chat_id, message_id, inline_message_id)"
            )
        out += [
            f"        return await self.bot.{snake(item['method'])}(",
            *[f"            {f['name']}={expression(f)}," for f in fields],
            "        )",
        ]

    out.append("")
    return "\n".join(out)


def main() -> None:
    spec = load_spec()
    generated, narrowed = generate(spec)
    (OUT / "generated.py").write_text(generated, encoding="utf-8")
    (OUT / "narrowed.py").write_text(narrowed, encoding="utf-8")
    (ROOT / "selfrot/context/accessors.py").write_text(
        generate_accessors(spec), encoding="utf-8"
    )
    (ROOT / "selfrot/handlers/kinds.py").write_text(
        generate_kinds(spec), encoding="utf-8"
    )
    (ROOT / "selfrot/filter/has.py").write_text(
        generate_has_filters(spec), encoding="utf-8"
    )
    check_method_names(spec)
    (ROOT / "selfrot/methods/generated.py").write_text(
        generate_methods(spec), encoding="utf-8"
    )
    (ROOT / "selfrot/client/methods.py").write_text(
        generate_bot_methods(spec), encoding="utf-8"
    )
    (ROOT / "selfrot/context/methods.py").write_text(
        generate_context_methods(spec), encoding="utf-8"
    )
    print(
        f"{spec['version']}: типов {len(spec['types'])}, "
        f"generated.py {len(generated.splitlines())} строк, "
        f"narrowed.py {len(narrowed.splitlines())} строк"
    )


if __name__ == "__main__":
    main()
