# АВТОГЕНЕРАЦИЯ: scripts/generate_types.py, Telegram Bot API 10.3, August 24, 2026.
# Руками не править — обновилась спека, перегенерировать.
# ruff: noqa
# Суженный тип переопределяет поле без значения по умолчанию
# (в рантайме он не создаётся, сужение типа при этом работает). Новые
# Pylance ругаются на каждое такое поле, поэтому правило выключено
# только в этом файле.
# pyright: reportGeneralTypeIssues=false
"""
Тип с гарантированно заполненным полем: <Поле><Тип> (TextMessage,
DataCallbackQuery). Такие типы есть для Message и для каждого объекта,
который Bot API кладёт в Update. Нужны для сужения типа (cast), в
рантайме отдельно не создаются. Комбинация гарантий одного типа —
наследование: class PhotoCaption(PhotoMessage, CaptionMessage, frozen=True).

Условие над ответом: Reply[<суженный тип ответа>], например Reply[UserMessage]
(ниже готовые алиасы ReplyUserMessage и другие). Условия над ответом тоже
складываются наследованием, но внутреннего типа: Reply[PhotoCaption].
"""
from __future__ import annotations

from typing import Generic, List, Literal, TypeVar, Union

from pydantic import ConfigDict, Field

from .generated import *


TReply = TypeVar("TReply", bound=Message)


class Reply(Message, Generic[TReply], frozen=True):
    """Message, у которого гарантированно есть `reply_to_message` суженного типа."""

    # Только для cast: в рантайме не создаётся, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    reply_to_message: TReply = Field()


class MessageThreadIdMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `message_thread_id`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    message_thread_id: int = Field()


class DirectMessagesTopicMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `direct_messages_topic`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    direct_messages_topic: DirectMessagesTopic = Field()


class UserMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `user`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    user: User = Field(alias='from')


class SenderChatMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `sender_chat`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    sender_chat: Chat = Field()


class SenderBoostCountMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `sender_boost_count`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    sender_boost_count: int = Field()


class SenderBusinessBotMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `sender_business_bot`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    sender_business_bot: User = Field()


class SenderTagMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `sender_tag`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    sender_tag: str = Field()


class ReceiverUserMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `receiver_user`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    receiver_user: User = Field()


class EphemeralMessageIdMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `ephemeral_message_id`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    ephemeral_message_id: int = Field()


class GuestQueryIdMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `guest_query_id`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    guest_query_id: str = Field()


class BusinessConnectionIdMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `business_connection_id`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    business_connection_id: str = Field()


class ForwardOriginMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `forward_origin`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    forward_origin: MessageOrigin = Field()


class IsTopicMessageMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `is_topic_message`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    is_topic_message: bool = Field()


class IsAutomaticForwardMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `is_automatic_forward`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    is_automatic_forward: bool = Field()


class ReplyToMessageMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `reply_to_message`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    reply_to_message: Message = Field()


class ExternalReplyMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `external_reply`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    external_reply: ExternalReplyInfo = Field()


class QuoteMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `quote`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    quote: TextQuote = Field()


class ReplyToStoryMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `reply_to_story`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    reply_to_story: Story = Field()


class ReplyToChecklistTaskIdMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `reply_to_checklist_task_id`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    reply_to_checklist_task_id: int = Field()


class ReplyToPollOptionIdMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `reply_to_poll_option_id`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    reply_to_poll_option_id: str = Field()


class ViaBotMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `via_bot`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    via_bot: User = Field()


class GuestBotCallerUserMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `guest_bot_caller_user`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    guest_bot_caller_user: User = Field()


class GuestBotCallerChatMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `guest_bot_caller_chat`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    guest_bot_caller_chat: Chat = Field()


class EditDateMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `edit_date`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    edit_date: int = Field()


class HasProtectedContentMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `has_protected_content`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    has_protected_content: bool = Field()


class IsFromOfflineMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `is_from_offline`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    is_from_offline: bool = Field()


class IsPaidPostMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `is_paid_post`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    is_paid_post: bool = Field()


class MediaGroupIdMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `media_group_id`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    media_group_id: str = Field()


class AuthorSignatureMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `author_signature`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    author_signature: str = Field()


class PaidStarCountMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `paid_star_count`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    paid_star_count: int = Field()


class TextMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `text`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    text: str = Field()


class EntitiesMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `entities`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    entities: List[MessageEntity] = Field()


class LinkPreviewOptionsMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `link_preview_options`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    link_preview_options: LinkPreviewOptions = Field()


class SuggestedPostInfoMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `suggested_post_info`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    suggested_post_info: SuggestedPostInfo = Field()


class EffectIdMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `effect_id`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    effect_id: str = Field()


class RichMessageMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `rich_message`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    rich_message: RichMessage = Field()


class AnimationMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `animation`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    animation: Animation = Field()


class AudioMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `audio`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    audio: Audio = Field()


class DocumentMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `document`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    document: Document = Field()


class LivePhotoMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `live_photo`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    live_photo: LivePhoto = Field()


class PaidMediaMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `paid_media`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    paid_media: PaidMediaInfo = Field()


class PhotoMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `photo`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    photo: List[PhotoSize] = Field()


class StickerMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `sticker`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    sticker: Sticker = Field()


class StoryMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `story`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    story: Story = Field()


class VideoMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `video`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    video: Video = Field()


class VideoNoteMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `video_note`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    video_note: VideoNote = Field()


class VoiceMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `voice`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    voice: Voice = Field()


class CaptionMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `caption`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    caption: str = Field()


class CaptionEntitiesMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `caption_entities`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    caption_entities: List[MessageEntity] = Field()


class ShowCaptionAboveMediaMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `show_caption_above_media`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    show_caption_above_media: bool = Field()


class HasMediaSpoilerMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `has_media_spoiler`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    has_media_spoiler: bool = Field()


class ChecklistMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `checklist`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    checklist: Checklist = Field()


class ContactMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `contact`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    contact: Contact = Field()


class DiceMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `dice`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    dice: Dice = Field()


class GameMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `game`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    game: Game = Field()


class PollMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `poll`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    poll: Poll = Field()


class VenueMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `venue`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    venue: Venue = Field()


class LocationMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `location`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    location: Location = Field()


class NewChatMembersMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `new_chat_members`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    new_chat_members: List[User] = Field()


class LeftChatMemberMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `left_chat_member`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    left_chat_member: User = Field()


class ChatOwnerLeftMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `chat_owner_left`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    chat_owner_left: ChatOwnerLeft = Field()


class ChatOwnerChangedMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `chat_owner_changed`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    chat_owner_changed: ChatOwnerChanged = Field()


class NewChatTitleMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `new_chat_title`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    new_chat_title: str = Field()


class NewChatPhotoMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `new_chat_photo`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    new_chat_photo: List[PhotoSize] = Field()


class DeleteChatPhotoMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `delete_chat_photo`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    delete_chat_photo: bool = Field()


class GroupChatCreatedMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `group_chat_created`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    group_chat_created: bool = Field()


class SupergroupChatCreatedMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `supergroup_chat_created`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    supergroup_chat_created: bool = Field()


class ChannelChatCreatedMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `channel_chat_created`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    channel_chat_created: bool = Field()


class MessageAutoDeleteTimerChangedMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `message_auto_delete_timer_changed`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    message_auto_delete_timer_changed: MessageAutoDeleteTimerChanged = Field()


class MigrateToChatIdMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `migrate_to_chat_id`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    migrate_to_chat_id: int = Field()


class MigrateFromChatIdMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `migrate_from_chat_id`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    migrate_from_chat_id: int = Field()


class PinnedMessageMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `pinned_message`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    pinned_message: MaybeInaccessibleMessage = Field()


class InvoiceMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `invoice`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    invoice: Invoice = Field()


class SuccessfulPaymentMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `successful_payment`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    successful_payment: SuccessfulPayment = Field()


class RefundedPaymentMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `refunded_payment`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    refunded_payment: RefundedPayment = Field()


class UsersSharedMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `users_shared`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    users_shared: UsersShared = Field()


class ChatSharedMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `chat_shared`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    chat_shared: ChatShared = Field()


class GiftMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `gift`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    gift: GiftInfo = Field()


class UniqueGiftMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `unique_gift`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    unique_gift: UniqueGiftInfo = Field()


class GiftUpgradeSentMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `gift_upgrade_sent`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    gift_upgrade_sent: GiftInfo = Field()


class ConnectedWebsiteMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `connected_website`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    connected_website: str = Field()


class WriteAccessAllowedMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `write_access_allowed`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    write_access_allowed: WriteAccessAllowed = Field()


class PassportDataMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `passport_data`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    passport_data: PassportData = Field()


class ProximityAlertTriggeredMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `proximity_alert_triggered`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    proximity_alert_triggered: ProximityAlertTriggered = Field()


class BoostAddedMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `boost_added`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    boost_added: ChatBoostAdded = Field()


class ChatBackgroundSetMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `chat_background_set`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    chat_background_set: ChatBackground = Field()


class ChecklistTasksDoneMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `checklist_tasks_done`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    checklist_tasks_done: ChecklistTasksDone = Field()


class ChecklistTasksAddedMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `checklist_tasks_added`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    checklist_tasks_added: ChecklistTasksAdded = Field()


class CommunityChatAddedMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `community_chat_added`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    community_chat_added: CommunityChatAdded = Field()


class CommunityChatJoinedMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `community_chat_joined`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    community_chat_joined: CommunityChatJoined = Field()


class CommunityChatRemovedMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `community_chat_removed`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    community_chat_removed: CommunityChatRemoved = Field()


class DirectMessagePriceChangedMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `direct_message_price_changed`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    direct_message_price_changed: DirectMessagePriceChanged = Field()


class ForumTopicCreatedMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `forum_topic_created`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    forum_topic_created: ForumTopicCreated = Field()


class ForumTopicEditedMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `forum_topic_edited`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    forum_topic_edited: ForumTopicEdited = Field()


class ForumTopicClosedMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `forum_topic_closed`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    forum_topic_closed: ForumTopicClosed = Field()


class ForumTopicReopenedMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `forum_topic_reopened`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    forum_topic_reopened: ForumTopicReopened = Field()


class GeneralForumTopicHiddenMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `general_forum_topic_hidden`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    general_forum_topic_hidden: GeneralForumTopicHidden = Field()


class GeneralForumTopicUnhiddenMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `general_forum_topic_unhidden`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    general_forum_topic_unhidden: GeneralForumTopicUnhidden = Field()


class GiveawayCreatedMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `giveaway_created`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    giveaway_created: GiveawayCreated = Field()


class GiveawayMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `giveaway`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    giveaway: Giveaway = Field()


class GiveawayWinnersMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `giveaway_winners`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    giveaway_winners: GiveawayWinners = Field()


class GiveawayCompletedMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `giveaway_completed`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    giveaway_completed: GiveawayCompleted = Field()


class ManagedBotCreatedMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `managed_bot_created`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    managed_bot_created: ManagedBotCreated = Field()


class PaidMessagePriceChangedMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `paid_message_price_changed`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    paid_message_price_changed: PaidMessagePriceChanged = Field()


class PollOptionAddedMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `poll_option_added`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    poll_option_added: PollOptionAdded = Field()


class PollOptionDeletedMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `poll_option_deleted`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    poll_option_deleted: PollOptionDeleted = Field()


class SuggestedPostApprovedMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `suggested_post_approved`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    suggested_post_approved: SuggestedPostApproved = Field()


class SuggestedPostApprovalFailedMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `suggested_post_approval_failed`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    suggested_post_approval_failed: SuggestedPostApprovalFailed = Field()


class SuggestedPostDeclinedMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `suggested_post_declined`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    suggested_post_declined: SuggestedPostDeclined = Field()


class SuggestedPostPaidMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `suggested_post_paid`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    suggested_post_paid: SuggestedPostPaid = Field()


class SuggestedPostRefundedMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `suggested_post_refunded`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    suggested_post_refunded: SuggestedPostRefunded = Field()


class VideoChatScheduledMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `video_chat_scheduled`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    video_chat_scheduled: VideoChatScheduled = Field()


class VideoChatStartedMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `video_chat_started`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    video_chat_started: VideoChatStarted = Field()


class VideoChatEndedMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `video_chat_ended`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    video_chat_ended: VideoChatEnded = Field()


class VideoChatParticipantsInvitedMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `video_chat_participants_invited`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    video_chat_participants_invited: VideoChatParticipantsInvited = Field()


class WebAppDataMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `web_app_data`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    web_app_data: WebAppData = Field()


class ReplyMarkupMessage(Message, frozen=True):
    """Message, у которого гарантированно есть `reply_markup`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    reply_markup: InlineKeyboardMarkup = Field()


class RightsBusinessConnection(BusinessConnection, frozen=True):
    """BusinessConnection, у которого гарантированно есть `rights`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    rights: BusinessBotRights = Field()


class UserMessageReactionUpdated(MessageReactionUpdated, frozen=True):
    """MessageReactionUpdated, у которого гарантированно есть `user`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    user: User = Field()


class ActorChatMessageReactionUpdated(MessageReactionUpdated, frozen=True):
    """MessageReactionUpdated, у которого гарантированно есть `actor_chat`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    actor_chat: Chat = Field()


class ChatTypeInlineQuery(InlineQuery, frozen=True):
    """InlineQuery, у которого гарантированно есть `chat_type`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    chat_type: str = Field()


class LocationInlineQuery(InlineQuery, frozen=True):
    """InlineQuery, у которого гарантированно есть `location`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    location: Location = Field()


class LocationChosenInlineResult(ChosenInlineResult, frozen=True):
    """ChosenInlineResult, у которого гарантированно есть `location`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    location: Location = Field()


class InlineMessageIdChosenInlineResult(ChosenInlineResult, frozen=True):
    """ChosenInlineResult, у которого гарантированно есть `inline_message_id`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    inline_message_id: str = Field()


class MessageCallbackQuery(CallbackQuery, frozen=True):
    """CallbackQuery, у которого гарантированно есть `message`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    message: MaybeInaccessibleMessage = Field()


class InlineMessageIdCallbackQuery(CallbackQuery, frozen=True):
    """CallbackQuery, у которого гарантированно есть `inline_message_id`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    inline_message_id: str = Field()


class DataCallbackQuery(CallbackQuery, frozen=True):
    """CallbackQuery, у которого гарантированно есть `data`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    data: str = Field()


class GameShortNameCallbackQuery(CallbackQuery, frozen=True):
    """CallbackQuery, у которого гарантированно есть `game_short_name`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    game_short_name: str = Field()


class ShippingOptionIdPreCheckoutQuery(PreCheckoutQuery, frozen=True):
    """PreCheckoutQuery, у которого гарантированно есть `shipping_option_id`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    shipping_option_id: str = Field()


class OrderInfoPreCheckoutQuery(PreCheckoutQuery, frozen=True):
    """PreCheckoutQuery, у которого гарантированно есть `order_info`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    order_info: OrderInfo = Field()


class QuestionEntitiesPoll(Poll, frozen=True):
    """Poll, у которого гарантированно есть `question_entities`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    question_entities: List[MessageEntity] = Field()


class CountryCodesPoll(Poll, frozen=True):
    """Poll, у которого гарантированно есть `country_codes`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    country_codes: List[str] = Field()


class CorrectOptionIdsPoll(Poll, frozen=True):
    """Poll, у которого гарантированно есть `correct_option_ids`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    correct_option_ids: List[int] = Field()


class ExplanationPoll(Poll, frozen=True):
    """Poll, у которого гарантированно есть `explanation`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    explanation: str = Field()


class ExplanationEntitiesPoll(Poll, frozen=True):
    """Poll, у которого гарантированно есть `explanation_entities`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    explanation_entities: List[MessageEntity] = Field()


class ExplanationMediaPoll(Poll, frozen=True):
    """Poll, у которого гарантированно есть `explanation_media`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    explanation_media: PollMedia = Field()


class OpenPeriodPoll(Poll, frozen=True):
    """Poll, у которого гарантированно есть `open_period`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    open_period: int = Field()


class CloseDatePoll(Poll, frozen=True):
    """Poll, у которого гарантированно есть `close_date`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    close_date: int = Field()


class DescriptionPoll(Poll, frozen=True):
    """Poll, у которого гарантированно есть `description`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    description: str = Field()


class DescriptionEntitiesPoll(Poll, frozen=True):
    """Poll, у которого гарантированно есть `description_entities`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    description_entities: List[MessageEntity] = Field()


class MediaPoll(Poll, frozen=True):
    """Poll, у которого гарантированно есть `media`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    media: PollMedia = Field()


class VoterChatPollAnswer(PollAnswer, frozen=True):
    """PollAnswer, у которого гарантированно есть `voter_chat`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    voter_chat: Chat = Field()


class UserPollAnswer(PollAnswer, frozen=True):
    """PollAnswer, у которого гарантированно есть `user`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    user: User = Field()


class InviteLinkChatMemberUpdated(ChatMemberUpdated, frozen=True):
    """ChatMemberUpdated, у которого гарантированно есть `invite_link`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    invite_link: ChatInviteLink = Field()


class ViaJoinRequestChatMemberUpdated(ChatMemberUpdated, frozen=True):
    """ChatMemberUpdated, у которого гарантированно есть `via_join_request`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    via_join_request: bool = Field()


class ViaChatFolderInviteLinkChatMemberUpdated(ChatMemberUpdated, frozen=True):
    """ChatMemberUpdated, у которого гарантированно есть `via_chat_folder_invite_link`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    via_chat_folder_invite_link: bool = Field()


class BioChatJoinRequest(ChatJoinRequest, frozen=True):
    """ChatJoinRequest, у которого гарантированно есть `bio`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    bio: str = Field()


class InviteLinkChatJoinRequest(ChatJoinRequest, frozen=True):
    """ChatJoinRequest, у которого гарантированно есть `invite_link`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    invite_link: ChatInviteLink = Field()


class QueryIdChatJoinRequest(ChatJoinRequest, frozen=True):
    """ChatJoinRequest, у которого гарантированно есть `query_id`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    query_id: str = Field()


class MessageThreadIdMessageGenerationStopped(MessageGenerationStopped, frozen=True):
    """MessageGenerationStopped, у которого гарантированно есть `message_thread_id`."""

    # Только для cast: в рантайме не создаются, сборка отложена.
    model_config = ConfigDict(defer_build=True)
    message_thread_id: int = Field()


# Готовые условия над ответом: Reply[<суженный тип>].
ReplyUserMessage = Reply[UserMessage]
ReplyTextMessage = Reply[TextMessage]
ReplyEntitiesMessage = Reply[EntitiesMessage]
ReplyCaptionMessage = Reply[CaptionMessage]
ReplyCaptionEntitiesMessage = Reply[CaptionEntitiesMessage]
ReplyPhotoMessage = Reply[PhotoMessage]
ReplyAnimationMessage = Reply[AnimationMessage]
ReplyAudioMessage = Reply[AudioMessage]
ReplyDocumentMessage = Reply[DocumentMessage]
ReplyStickerMessage = Reply[StickerMessage]
ReplyVideoMessage = Reply[VideoMessage]
ReplyVideoNoteMessage = Reply[VideoNoteMessage]
ReplyVoiceMessage = Reply[VoiceMessage]


__all__ = [
    "Reply",
    "ReplyUserMessage",
    "ReplyTextMessage",
    "ReplyEntitiesMessage",
    "ReplyCaptionMessage",
    "ReplyCaptionEntitiesMessage",
    "ReplyPhotoMessage",
    "ReplyAnimationMessage",
    "ReplyAudioMessage",
    "ReplyDocumentMessage",
    "ReplyStickerMessage",
    "ReplyVideoMessage",
    "ReplyVideoNoteMessage",
    "ReplyVoiceMessage",
    "MessageThreadIdMessage",
    "DirectMessagesTopicMessage",
    "UserMessage",
    "SenderChatMessage",
    "SenderBoostCountMessage",
    "SenderBusinessBotMessage",
    "SenderTagMessage",
    "ReceiverUserMessage",
    "EphemeralMessageIdMessage",
    "GuestQueryIdMessage",
    "BusinessConnectionIdMessage",
    "ForwardOriginMessage",
    "IsTopicMessageMessage",
    "IsAutomaticForwardMessage",
    "ReplyToMessageMessage",
    "ExternalReplyMessage",
    "QuoteMessage",
    "ReplyToStoryMessage",
    "ReplyToChecklistTaskIdMessage",
    "ReplyToPollOptionIdMessage",
    "ViaBotMessage",
    "GuestBotCallerUserMessage",
    "GuestBotCallerChatMessage",
    "EditDateMessage",
    "HasProtectedContentMessage",
    "IsFromOfflineMessage",
    "IsPaidPostMessage",
    "MediaGroupIdMessage",
    "AuthorSignatureMessage",
    "PaidStarCountMessage",
    "TextMessage",
    "EntitiesMessage",
    "LinkPreviewOptionsMessage",
    "SuggestedPostInfoMessage",
    "EffectIdMessage",
    "RichMessageMessage",
    "AnimationMessage",
    "AudioMessage",
    "DocumentMessage",
    "LivePhotoMessage",
    "PaidMediaMessage",
    "PhotoMessage",
    "StickerMessage",
    "StoryMessage",
    "VideoMessage",
    "VideoNoteMessage",
    "VoiceMessage",
    "CaptionMessage",
    "CaptionEntitiesMessage",
    "ShowCaptionAboveMediaMessage",
    "HasMediaSpoilerMessage",
    "ChecklistMessage",
    "ContactMessage",
    "DiceMessage",
    "GameMessage",
    "PollMessage",
    "VenueMessage",
    "LocationMessage",
    "NewChatMembersMessage",
    "LeftChatMemberMessage",
    "ChatOwnerLeftMessage",
    "ChatOwnerChangedMessage",
    "NewChatTitleMessage",
    "NewChatPhotoMessage",
    "DeleteChatPhotoMessage",
    "GroupChatCreatedMessage",
    "SupergroupChatCreatedMessage",
    "ChannelChatCreatedMessage",
    "MessageAutoDeleteTimerChangedMessage",
    "MigrateToChatIdMessage",
    "MigrateFromChatIdMessage",
    "PinnedMessageMessage",
    "InvoiceMessage",
    "SuccessfulPaymentMessage",
    "RefundedPaymentMessage",
    "UsersSharedMessage",
    "ChatSharedMessage",
    "GiftMessage",
    "UniqueGiftMessage",
    "GiftUpgradeSentMessage",
    "ConnectedWebsiteMessage",
    "WriteAccessAllowedMessage",
    "PassportDataMessage",
    "ProximityAlertTriggeredMessage",
    "BoostAddedMessage",
    "ChatBackgroundSetMessage",
    "ChecklistTasksDoneMessage",
    "ChecklistTasksAddedMessage",
    "CommunityChatAddedMessage",
    "CommunityChatJoinedMessage",
    "CommunityChatRemovedMessage",
    "DirectMessagePriceChangedMessage",
    "ForumTopicCreatedMessage",
    "ForumTopicEditedMessage",
    "ForumTopicClosedMessage",
    "ForumTopicReopenedMessage",
    "GeneralForumTopicHiddenMessage",
    "GeneralForumTopicUnhiddenMessage",
    "GiveawayCreatedMessage",
    "GiveawayMessage",
    "GiveawayWinnersMessage",
    "GiveawayCompletedMessage",
    "ManagedBotCreatedMessage",
    "PaidMessagePriceChangedMessage",
    "PollOptionAddedMessage",
    "PollOptionDeletedMessage",
    "SuggestedPostApprovedMessage",
    "SuggestedPostApprovalFailedMessage",
    "SuggestedPostDeclinedMessage",
    "SuggestedPostPaidMessage",
    "SuggestedPostRefundedMessage",
    "VideoChatScheduledMessage",
    "VideoChatStartedMessage",
    "VideoChatEndedMessage",
    "VideoChatParticipantsInvitedMessage",
    "WebAppDataMessage",
    "ReplyMarkupMessage",
    "RightsBusinessConnection",
    "UserMessageReactionUpdated",
    "ActorChatMessageReactionUpdated",
    "ChatTypeInlineQuery",
    "LocationInlineQuery",
    "LocationChosenInlineResult",
    "InlineMessageIdChosenInlineResult",
    "MessageCallbackQuery",
    "InlineMessageIdCallbackQuery",
    "DataCallbackQuery",
    "GameShortNameCallbackQuery",
    "ShippingOptionIdPreCheckoutQuery",
    "OrderInfoPreCheckoutQuery",
    "QuestionEntitiesPoll",
    "CountryCodesPoll",
    "CorrectOptionIdsPoll",
    "ExplanationPoll",
    "ExplanationEntitiesPoll",
    "ExplanationMediaPoll",
    "OpenPeriodPoll",
    "CloseDatePoll",
    "DescriptionPoll",
    "DescriptionEntitiesPoll",
    "MediaPoll",
    "VoterChatPollAnswer",
    "UserPollAnswer",
    "InviteLinkChatMemberUpdated",
    "ViaJoinRequestChatMemberUpdated",
    "ViaChatFolderInviteLinkChatMemberUpdated",
    "BioChatJoinRequest",
    "InviteLinkChatJoinRequest",
    "QueryIdChatJoinRequest",
    "MessageThreadIdMessageGenerationStopped",
]
