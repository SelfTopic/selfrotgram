from collections.abc import Iterable
from typing import Any

from ..context import BaseContext
from ..exceptions import DefinitionError
from ..types import ChatMember, ChatMemberRestricted, ChatMemberUpdated
from .base import BaseFilter

STATUSES = ("creator", "administrator", "member", "restricted", "left", "kicked")
_IN_CHAT = ("creator", "administrator", "member")


def is_member(member: ChatMember) -> bool:
    """
    Находится ли пользователь в чате. У restricted («ограничен») два смысла:
    ограничен, но в чате, и ограничен, но вышел; это различает is_member.
    """
    if isinstance(member, ChatMemberRestricted):
        return member.is_member

    return member.status in _IN_CHAT


class MemberFilter(BaseFilter[BaseContext[ChatMemberUpdated]]):
    """
    Основа фильтров по изменению статуса участника. Работает и в
    MyChatMemberHandler (статус самого бота), и в ChatMemberHandler (статус других).
    """

    guarantees = ChatMemberUpdated

    def _event(self, ctx: BaseContext[Any]) -> ChatMemberUpdated | None:
        event = ctx.event
        return event if isinstance(event, ChatMemberUpdated) else None

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = self._event(ctx)
        return event is not None and self._test(event)

    def _test(self, event: ChatMemberUpdated) -> bool:
        raise NotImplementedError


class MemberJoined(MemberFilter):
    """Раньше не был в чате, теперь в чате (вошёл, добавлен, одобрена заявка)."""

    def _test(self, event: ChatMemberUpdated) -> bool:
        return not is_member(event.old_chat_member) and is_member(event.new_chat_member)


class MemberLeft(MemberFilter):
    """Раньше был в чате, теперь нет (вышел, удалён, заблокирован)."""

    def _test(self, event: ChatMemberUpdated) -> bool:
        return is_member(event.old_chat_member) and not is_member(event.new_chat_member)


def _statuses(
    value: str | Iterable[str] | None, argument: str
) -> frozenset[str] | None:
    if value is None:
        return None

    found = frozenset([value] if isinstance(value, str) else value)
    unknown = found - set(STATUSES)
    if unknown:
        raise DefinitionError(
            f"ChatMemberTransition({argument}=...): нет статусов {sorted(unknown)}; "
            f"бывают {', '.join(STATUSES)}"
        )

    return found


class ChatMemberTransition(MemberFilter):
    """
    Переход между конкретными статусами. None — любой:

        ChatMemberTransition(before="member", after="administrator")   # повышен
        ChatMemberTransition(after="kicked")                           # заблокирован
        ChatMemberTransition(before={"left", "kicked"}, after="member")
    """

    def __init__(
        self,
        *,
        before: str | Iterable[str] | None = None,
        after: str | Iterable[str] | None = None,
    ) -> None:
        self.before = _statuses(before, "before")
        self.after = _statuses(after, "after")

    def _test(self, event: ChatMemberUpdated) -> bool:
        return (
            self.before is None or event.old_chat_member.status in self.before
        ) and (self.after is None or event.new_chat_member.status in self.after)

    def __repr__(self) -> str:
        return (
            f"ChatMemberTransition(before={sorted(self.before or [])}, "
            f"after={sorted(self.after or [])})"
        )
