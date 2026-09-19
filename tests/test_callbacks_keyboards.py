from enum import Enum
from typing import Literal

import pytest

from selfrot import BaseContext, Bot, CallbackPayload, InlineKeyboard, button
from selfrot.exceptions import (
    CallbackDataError,
    DefinitionError,
    FilterMatchError,
    KeyboardError,
)
from selfrot.filter import ChatMemberTransition, MemberJoined, MemberLeft
from selfrot.types import ChatMemberUpdated

from .conftest import TOKEN, bind, callback_update


class Color(Enum):
    RED = "r"
    BLUE = "b"


class Duel(CallbackPayload, prefix="duel"):
    duel_id: int
    action: Literal["consent", "fora", "outcome"]
    expected_id: int


class Mixed(CallbackPayload, prefix="mx", sep="|"):
    flag: bool
    color: Color
    note: str | None = None
    n: int | None = None


def ctx(raw: dict) -> BaseContext:
    api = Bot(TOKEN)
    return BaseContext(bind(raw, api), api)


class TestCallbackPayload:
    def test_pack_matches_hand_written_format(self):
        assert (
            Duel(duel_id=12, action="consent", expected_id=5).pack()
            == "duel:12:consent:5"
        )

    def test_roundtrip_restores_types(self):
        data = Duel.unpack("duel:12:consent:5")
        assert data == Duel(duel_id=12, action="consent", expected_id=5)
        assert isinstance(data.duel_id, int)

    def test_bool_enum_optional_and_custom_separator(self):
        packed = Mixed(flag=True, color=Color.BLUE, note=None, n=7).pack()
        assert packed == "mx|1|b||7"
        assert Mixed.unpack(packed) == Mixed(
            flag=True, color=Color.BLUE, note=None, n=7
        )
        assert Mixed.unpack("mx|0|r|привет|").note == "привет"

    @pytest.mark.parametrize(
        "data",
        [
            "quiz:12:consent:5",
            "duel:12:consent",
            "duel:x:consent:5",
            "duel:1:hack:5",
            "мусор",
        ],
    )
    def test_bad_data(self, data):
        with pytest.raises(CallbackDataError):
            Duel.unpack(data)
        assert Duel.try_unpack(data) is None

    def test_separator_inside_value(self):
        with pytest.raises(CallbackDataError, match="разделитель"):
            Mixed(flag=True, color=Color.RED, note="a|b").pack()

    def test_over_64_bytes_counts_bytes_not_chars(self):
        class Long(CallbackPayload, prefix="quiz"):
            text: str

        with pytest.raises(CallbackDataError, match="64"):
            Long(text="я" * 30).pack()  # 30 символов, но 60 байт плюс префикс

    @pytest.mark.parametrize("prefix", ["", "a:b"])
    def test_bad_prefix(self, prefix):
        with pytest.raises(DefinitionError):
            type("Bad", (CallbackPayload,), {}, prefix=prefix)


class TestPayloadFilter:
    async def test_filter_and_parse(self):
        flt = Duel.filter(action="consent")
        context = ctx(callback_update("duel:3:consent:7"))
        assert await flt.check(context)
        assert flt.parse(context).duel_id == 3

    async def test_field_condition_and_foreign_data(self):
        flt = Duel.filter(action="consent")
        assert not await flt.check(ctx(callback_update("duel:3:fora:7")))
        assert not await flt.check(ctx(callback_update("quiz_answer_1_0")))

    def test_unknown_field_is_definition_error(self):
        with pytest.raises(DefinitionError, match="actoin"):
            Duel.filter(actoin="x")

    async def test_or_of_filters(self):
        flt = Duel.filter(action="fora") | Duel.filter(action="outcome")
        assert await flt.check(ctx(callback_update("duel:1:outcome:2")))
        assert not await flt.check(ctx(callback_update("duel:1:consent:2")))

    async def test_pressed_by_owner_only(self):
        owned = Duel.filter(action="consent").pressed_by("expected_id")
        assert await owned.check(ctx(callback_update("duel:1:consent:7", uid=7)))
        assert not await owned.check(ctx(callback_update("duel:1:consent:7", uid=8)))

    def test_pressed_by_returns_copy_and_validates_field(self):
        base = Duel.filter(action="consent")
        owned = base.pressed_by("expected_id")
        assert base.owner_field is None
        assert owned.owner_field == "expected_id"
        assert repr(owned) == "Duel.filter(action='consent').pressed_by('expected_id')"
        with pytest.raises(DefinitionError):
            base.pressed_by("nobody")

    async def test_parse_without_match_raises(self):
        with pytest.raises(FilterMatchError):
            Duel.filter().parse(ctx(callback_update("quiz:1")))


class TestKeyboard:
    def test_width_lays_buttons_in_rows(self):
        kb = InlineKeyboard(width=2)
        for i in range(5):
            kb.button(f"вариант {i}", f"a_{i}")
        assert [len(r) for r in kb.markup().inline_keyboard] == [2, 2, 1]

    def test_row_is_its_own_row(self):
        kb = InlineKeyboard(width=2).button("a", "1").button("b", "2")
        kb.row(button("Пропустить", "skip"), button("Сайт", url="https://example.org"))
        kb.button("после", "3")
        rows = kb.markup().inline_keyboard
        assert [len(r) for r in rows] == [2, 2, 1]
        assert rows[1][1].url == "https://example.org"

    def test_payload_and_style(self):
        made = button(
            "Принять", Duel(duel_id=1, action="fora", expected_id=2), style="success"
        )
        assert made.callback_data == "duel:1:fora:2"
        assert made.style == "success"

    def test_default_is_one_per_row_and_empty_is_allowed(self):
        assert [
            len(r)
            for r in InlineKeyboard()
            .button("a", "1")
            .button("b", "2")
            .markup()
            .inline_keyboard
        ] == [1, 1]
        assert InlineKeyboard().markup().inline_keyboard == []

    @pytest.mark.parametrize(
        ("build", "error"),
        [
            (lambda: button("x", "d", url="https://a.b"), KeyboardError),  # два вида
            (lambda: button("x"), KeyboardError),  # ни одного
            (lambda: button("x", ulr="https://a.b"), KeyboardError),  # опечатка
            (lambda: button("x", "a" * 65), CallbackDataError),
            (lambda: button("x", ""), CallbackDataError),
            (lambda: InlineKeyboard(width=9), KeyboardError),
            (
                lambda: InlineKeyboard().row(
                    *[button(str(i), str(i)) for i in range(9)]
                ),
                KeyboardError,
            ),
        ],
    )
    def test_telegram_limits_checked_before_sending(self, build, error):
        with pytest.raises(error):
            build()

    def test_100_button_limit(self):
        kb = InlineKeyboard()
        for i in range(100):
            kb.button(str(i), str(i))
        with pytest.raises(KeyboardError):
            kb.button("лишняя", "x")

    def test_serialization_has_no_none_fields(self):
        dumped = (
            InlineKeyboard()
            .button("a", "1")
            .markup()
            .model_dump(mode="json", exclude_none=True)
        )
        assert dumped == {"inline_keyboard": [[{"text": "a", "callback_data": "1"}]]}


ADMIN = {
    "can_be_edited": False,
    "is_anonymous": False,
    "can_manage_chat": True,
    "can_delete_messages": True,
    "can_manage_video_chats": True,
    "can_restrict_members": True,
    "can_promote_members": True,
    "can_change_info": True,
    "can_invite_users": True,
    "can_post_stories": True,
    "can_edit_stories": True,
    "can_delete_stories": True,
    "can_send_welcome_messages": True,
}
RESTRICTED = {
    name: False
    for name in (
        "can_send_messages",
        "can_send_audios",
        "can_send_documents",
        "can_send_photos",
        "can_send_videos",
        "can_send_video_notes",
        "can_send_voice_notes",
        "can_send_polls",
        "can_send_other_messages",
        "can_add_web_page_previews",
        "can_change_info",
        "can_invite_users",
        "can_pin_messages",
        "can_manage_topics",
        "can_react_to_messages",
        "can_edit_tag",
    )
}
USER = {"id": 7, "is_bot": False, "first_name": "u"}


def status(name: str, **extra) -> dict:
    return {"status": name, "user": USER, **extra}


def transition(old: dict, new: dict) -> BaseContext:
    event = {
        "chat": {"id": -100, "type": "supergroup", "title": "g"},
        "from": USER,
        "date": 0,
        "old_chat_member": old,
        "new_chat_member": new,
    }
    ctx_ = ctx({"update_id": 1, "chat_member": event})
    assert isinstance(ctx_.event, ChatMemberUpdated)
    return ctx_


class TestMemberFilters:
    @pytest.mark.parametrize(
        ("old", "new", "joined", "left"),
        [
            (status("left"), status("member"), True, False),
            (status("kicked", until_date=0), status("member"), True, False),
            (status("left"), status("administrator", **ADMIN), True, False),
            (status("member"), status("left"), False, True),
            (
                status("member"),
                status("kicked", until_date=0),
                False,
                True,
            ),  # бан — тоже выход
            (status("member"), status("member"), False, False),
            (status("left"), status("left"), False, False),
            (status("kicked", until_date=0), status("left"), False, False),
            (
                status("left"),
                status("restricted", is_member=True, until_date=0, **RESTRICTED),
                True,
                False,
            ),
            (
                status("left"),
                status("restricted", is_member=False, until_date=0, **RESTRICTED),
                False,
                False,
            ),
            (
                status("member"),
                status("restricted", is_member=True, until_date=0, **RESTRICTED),
                False,
                False,
            ),
            (
                status("restricted", is_member=True, until_date=0, **RESTRICTED),
                status("left"),
                False,
                True,
            ),
        ],
    )
    async def test_joined_and_left(self, old, new, joined, left):
        context = transition(old, new)
        assert await MemberJoined().check(context) is joined
        assert await MemberLeft().check(context) is left

    async def test_transition_by_status_names(self):
        promoted = ChatMemberTransition(before="member", after="administrator")
        assert await promoted.check(
            transition(status("member"), status("administrator", **ADMIN))
        )
        assert not await promoted.check(
            transition(status("left"), status("administrator", **ADMIN))
        )
        banned = ChatMemberTransition(after={"kicked"})
        assert await banned.check(
            transition(status("left"), status("kicked", until_date=0))
        )

    def test_typo_in_status(self):
        with pytest.raises(DefinitionError, match="banned"):
            ChatMemberTransition(after="banned")
