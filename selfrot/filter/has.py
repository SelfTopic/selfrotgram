# АВТОГЕНЕРАЦИЯ: scripts/generate_types.py, Telegram Bot API 10.3, August 24, 2026.
# Руками не править — обновилась спека, перегенерировать.
# ruff: noqa
"""
Фильтры «у объекта апдейта заполнено поле»: по одному на каждый суженный тип.
HasText гарантирует TextMessage, HasDataCallbackQuery — DataCallbackQuery.
"""
from __future__ import annotations

from typing import Any

from ..context import BaseContext
from ..types import *
from .base import BaseFilter


class HasMessageThreadId(BaseFilter[BaseContext[MessageThreadIdMessage]]):
    """У объекта Message заполнено `message_thread_id`. Гарантирует MessageThreadIdMessage."""

    guarantees = MessageThreadIdMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.message_thread_id is not None


class HasDirectMessagesTopic(BaseFilter[BaseContext[DirectMessagesTopicMessage]]):
    """У объекта Message заполнено `direct_messages_topic`. Гарантирует DirectMessagesTopicMessage."""

    guarantees = DirectMessagesTopicMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.direct_messages_topic is not None


class HasUser(BaseFilter[BaseContext[UserMessage]]):
    """У объекта Message заполнено `user`. Гарантирует UserMessage."""

    guarantees = UserMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.user is not None


class HasSenderChat(BaseFilter[BaseContext[SenderChatMessage]]):
    """У объекта Message заполнено `sender_chat`. Гарантирует SenderChatMessage."""

    guarantees = SenderChatMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.sender_chat is not None


class HasSenderBoostCount(BaseFilter[BaseContext[SenderBoostCountMessage]]):
    """У объекта Message заполнено `sender_boost_count`. Гарантирует SenderBoostCountMessage."""

    guarantees = SenderBoostCountMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.sender_boost_count is not None


class HasSenderBusinessBot(BaseFilter[BaseContext[SenderBusinessBotMessage]]):
    """У объекта Message заполнено `sender_business_bot`. Гарантирует SenderBusinessBotMessage."""

    guarantees = SenderBusinessBotMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.sender_business_bot is not None


class HasSenderTag(BaseFilter[BaseContext[SenderTagMessage]]):
    """У объекта Message заполнено `sender_tag`. Гарантирует SenderTagMessage."""

    guarantees = SenderTagMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.sender_tag is not None


class HasReceiverUser(BaseFilter[BaseContext[ReceiverUserMessage]]):
    """У объекта Message заполнено `receiver_user`. Гарантирует ReceiverUserMessage."""

    guarantees = ReceiverUserMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.receiver_user is not None


class HasEphemeralMessageId(BaseFilter[BaseContext[EphemeralMessageIdMessage]]):
    """У объекта Message заполнено `ephemeral_message_id`. Гарантирует EphemeralMessageIdMessage."""

    guarantees = EphemeralMessageIdMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.ephemeral_message_id is not None


class HasGuestQueryId(BaseFilter[BaseContext[GuestQueryIdMessage]]):
    """У объекта Message заполнено `guest_query_id`. Гарантирует GuestQueryIdMessage."""

    guarantees = GuestQueryIdMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.guest_query_id is not None


class HasBusinessConnectionId(BaseFilter[BaseContext[BusinessConnectionIdMessage]]):
    """У объекта Message заполнено `business_connection_id`. Гарантирует BusinessConnectionIdMessage."""

    guarantees = BusinessConnectionIdMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.business_connection_id is not None


class HasForwardOrigin(BaseFilter[BaseContext[ForwardOriginMessage]]):
    """У объекта Message заполнено `forward_origin`. Гарантирует ForwardOriginMessage."""

    guarantees = ForwardOriginMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.forward_origin is not None


class HasIsTopicMessage(BaseFilter[BaseContext[IsTopicMessageMessage]]):
    """У объекта Message заполнено `is_topic_message`. Гарантирует IsTopicMessageMessage."""

    guarantees = IsTopicMessageMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.is_topic_message is not None


class HasIsAutomaticForward(BaseFilter[BaseContext[IsAutomaticForwardMessage]]):
    """У объекта Message заполнено `is_automatic_forward`. Гарантирует IsAutomaticForwardMessage."""

    guarantees = IsAutomaticForwardMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.is_automatic_forward is not None


class HasReplyToMessage(BaseFilter[BaseContext[ReplyToMessageMessage]]):
    """У объекта Message заполнено `reply_to_message`. Гарантирует ReplyToMessageMessage."""

    guarantees = ReplyToMessageMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.reply_to_message is not None


class HasExternalReply(BaseFilter[BaseContext[ExternalReplyMessage]]):
    """У объекта Message заполнено `external_reply`. Гарантирует ExternalReplyMessage."""

    guarantees = ExternalReplyMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.external_reply is not None


class HasQuote(BaseFilter[BaseContext[QuoteMessage]]):
    """У объекта Message заполнено `quote`. Гарантирует QuoteMessage."""

    guarantees = QuoteMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.quote is not None


class HasReplyToStory(BaseFilter[BaseContext[ReplyToStoryMessage]]):
    """У объекта Message заполнено `reply_to_story`. Гарантирует ReplyToStoryMessage."""

    guarantees = ReplyToStoryMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.reply_to_story is not None


class HasReplyToChecklistTaskId(BaseFilter[BaseContext[ReplyToChecklistTaskIdMessage]]):
    """У объекта Message заполнено `reply_to_checklist_task_id`. Гарантирует ReplyToChecklistTaskIdMessage."""

    guarantees = ReplyToChecklistTaskIdMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.reply_to_checklist_task_id is not None


class HasReplyToPollOptionId(BaseFilter[BaseContext[ReplyToPollOptionIdMessage]]):
    """У объекта Message заполнено `reply_to_poll_option_id`. Гарантирует ReplyToPollOptionIdMessage."""

    guarantees = ReplyToPollOptionIdMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.reply_to_poll_option_id is not None


class HasViaBot(BaseFilter[BaseContext[ViaBotMessage]]):
    """У объекта Message заполнено `via_bot`. Гарантирует ViaBotMessage."""

    guarantees = ViaBotMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.via_bot is not None


class HasGuestBotCallerUser(BaseFilter[BaseContext[GuestBotCallerUserMessage]]):
    """У объекта Message заполнено `guest_bot_caller_user`. Гарантирует GuestBotCallerUserMessage."""

    guarantees = GuestBotCallerUserMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.guest_bot_caller_user is not None


class HasGuestBotCallerChat(BaseFilter[BaseContext[GuestBotCallerChatMessage]]):
    """У объекта Message заполнено `guest_bot_caller_chat`. Гарантирует GuestBotCallerChatMessage."""

    guarantees = GuestBotCallerChatMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.guest_bot_caller_chat is not None


class HasEditDate(BaseFilter[BaseContext[EditDateMessage]]):
    """У объекта Message заполнено `edit_date`. Гарантирует EditDateMessage."""

    guarantees = EditDateMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.edit_date is not None


class HasHasProtectedContent(BaseFilter[BaseContext[HasProtectedContentMessage]]):
    """У объекта Message заполнено `has_protected_content`. Гарантирует HasProtectedContentMessage."""

    guarantees = HasProtectedContentMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.has_protected_content is not None


class HasIsFromOffline(BaseFilter[BaseContext[IsFromOfflineMessage]]):
    """У объекта Message заполнено `is_from_offline`. Гарантирует IsFromOfflineMessage."""

    guarantees = IsFromOfflineMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.is_from_offline is not None


class HasIsPaidPost(BaseFilter[BaseContext[IsPaidPostMessage]]):
    """У объекта Message заполнено `is_paid_post`. Гарантирует IsPaidPostMessage."""

    guarantees = IsPaidPostMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.is_paid_post is not None


class HasMediaGroupId(BaseFilter[BaseContext[MediaGroupIdMessage]]):
    """У объекта Message заполнено `media_group_id`. Гарантирует MediaGroupIdMessage."""

    guarantees = MediaGroupIdMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.media_group_id is not None


class HasAuthorSignature(BaseFilter[BaseContext[AuthorSignatureMessage]]):
    """У объекта Message заполнено `author_signature`. Гарантирует AuthorSignatureMessage."""

    guarantees = AuthorSignatureMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.author_signature is not None


class HasPaidStarCount(BaseFilter[BaseContext[PaidStarCountMessage]]):
    """У объекта Message заполнено `paid_star_count`. Гарантирует PaidStarCountMessage."""

    guarantees = PaidStarCountMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.paid_star_count is not None


class HasText(BaseFilter[BaseContext[TextMessage]]):
    """У объекта Message заполнено `text`. Гарантирует TextMessage."""

    guarantees = TextMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.text is not None


class HasEntities(BaseFilter[BaseContext[EntitiesMessage]]):
    """У объекта Message заполнено `entities`. Гарантирует EntitiesMessage."""

    guarantees = EntitiesMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.entities is not None


class HasLinkPreviewOptions(BaseFilter[BaseContext[LinkPreviewOptionsMessage]]):
    """У объекта Message заполнено `link_preview_options`. Гарантирует LinkPreviewOptionsMessage."""

    guarantees = LinkPreviewOptionsMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.link_preview_options is not None


class HasSuggestedPostInfo(BaseFilter[BaseContext[SuggestedPostInfoMessage]]):
    """У объекта Message заполнено `suggested_post_info`. Гарантирует SuggestedPostInfoMessage."""

    guarantees = SuggestedPostInfoMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.suggested_post_info is not None


class HasEffectId(BaseFilter[BaseContext[EffectIdMessage]]):
    """У объекта Message заполнено `effect_id`. Гарантирует EffectIdMessage."""

    guarantees = EffectIdMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.effect_id is not None


class HasRichMessage(BaseFilter[BaseContext[RichMessageMessage]]):
    """У объекта Message заполнено `rich_message`. Гарантирует RichMessageMessage."""

    guarantees = RichMessageMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.rich_message is not None


class HasAnimation(BaseFilter[BaseContext[AnimationMessage]]):
    """У объекта Message заполнено `animation`. Гарантирует AnimationMessage."""

    guarantees = AnimationMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.animation is not None


class HasAudio(BaseFilter[BaseContext[AudioMessage]]):
    """У объекта Message заполнено `audio`. Гарантирует AudioMessage."""

    guarantees = AudioMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.audio is not None


class HasDocument(BaseFilter[BaseContext[DocumentMessage]]):
    """У объекта Message заполнено `document`. Гарантирует DocumentMessage."""

    guarantees = DocumentMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.document is not None


class HasLivePhoto(BaseFilter[BaseContext[LivePhotoMessage]]):
    """У объекта Message заполнено `live_photo`. Гарантирует LivePhotoMessage."""

    guarantees = LivePhotoMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.live_photo is not None


class HasPaidMedia(BaseFilter[BaseContext[PaidMediaMessage]]):
    """У объекта Message заполнено `paid_media`. Гарантирует PaidMediaMessage."""

    guarantees = PaidMediaMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.paid_media is not None


class HasPhoto(BaseFilter[BaseContext[PhotoMessage]]):
    """У объекта Message заполнено `photo`. Гарантирует PhotoMessage."""

    guarantees = PhotoMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.photo is not None


class HasSticker(BaseFilter[BaseContext[StickerMessage]]):
    """У объекта Message заполнено `sticker`. Гарантирует StickerMessage."""

    guarantees = StickerMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.sticker is not None


class HasStory(BaseFilter[BaseContext[StoryMessage]]):
    """У объекта Message заполнено `story`. Гарантирует StoryMessage."""

    guarantees = StoryMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.story is not None


class HasVideo(BaseFilter[BaseContext[VideoMessage]]):
    """У объекта Message заполнено `video`. Гарантирует VideoMessage."""

    guarantees = VideoMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.video is not None


class HasVideoNote(BaseFilter[BaseContext[VideoNoteMessage]]):
    """У объекта Message заполнено `video_note`. Гарантирует VideoNoteMessage."""

    guarantees = VideoNoteMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.video_note is not None


class HasVoice(BaseFilter[BaseContext[VoiceMessage]]):
    """У объекта Message заполнено `voice`. Гарантирует VoiceMessage."""

    guarantees = VoiceMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.voice is not None


class HasCaption(BaseFilter[BaseContext[CaptionMessage]]):
    """У объекта Message заполнено `caption`. Гарантирует CaptionMessage."""

    guarantees = CaptionMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.caption is not None


class HasCaptionEntities(BaseFilter[BaseContext[CaptionEntitiesMessage]]):
    """У объекта Message заполнено `caption_entities`. Гарантирует CaptionEntitiesMessage."""

    guarantees = CaptionEntitiesMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.caption_entities is not None


class HasShowCaptionAboveMedia(BaseFilter[BaseContext[ShowCaptionAboveMediaMessage]]):
    """У объекта Message заполнено `show_caption_above_media`. Гарантирует ShowCaptionAboveMediaMessage."""

    guarantees = ShowCaptionAboveMediaMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.show_caption_above_media is not None


class HasHasMediaSpoiler(BaseFilter[BaseContext[HasMediaSpoilerMessage]]):
    """У объекта Message заполнено `has_media_spoiler`. Гарантирует HasMediaSpoilerMessage."""

    guarantees = HasMediaSpoilerMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.has_media_spoiler is not None


class HasChecklist(BaseFilter[BaseContext[ChecklistMessage]]):
    """У объекта Message заполнено `checklist`. Гарантирует ChecklistMessage."""

    guarantees = ChecklistMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.checklist is not None


class HasContact(BaseFilter[BaseContext[ContactMessage]]):
    """У объекта Message заполнено `contact`. Гарантирует ContactMessage."""

    guarantees = ContactMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.contact is not None


class HasDice(BaseFilter[BaseContext[DiceMessage]]):
    """У объекта Message заполнено `dice`. Гарантирует DiceMessage."""

    guarantees = DiceMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.dice is not None


class HasGame(BaseFilter[BaseContext[GameMessage]]):
    """У объекта Message заполнено `game`. Гарантирует GameMessage."""

    guarantees = GameMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.game is not None


class HasPoll(BaseFilter[BaseContext[PollMessage]]):
    """У объекта Message заполнено `poll`. Гарантирует PollMessage."""

    guarantees = PollMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.poll is not None


class HasVenue(BaseFilter[BaseContext[VenueMessage]]):
    """У объекта Message заполнено `venue`. Гарантирует VenueMessage."""

    guarantees = VenueMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.venue is not None


class HasLocation(BaseFilter[BaseContext[LocationMessage]]):
    """У объекта Message заполнено `location`. Гарантирует LocationMessage."""

    guarantees = LocationMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.location is not None


class HasNewChatMembers(BaseFilter[BaseContext[NewChatMembersMessage]]):
    """У объекта Message заполнено `new_chat_members`. Гарантирует NewChatMembersMessage."""

    guarantees = NewChatMembersMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.new_chat_members is not None


class HasLeftChatMember(BaseFilter[BaseContext[LeftChatMemberMessage]]):
    """У объекта Message заполнено `left_chat_member`. Гарантирует LeftChatMemberMessage."""

    guarantees = LeftChatMemberMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.left_chat_member is not None


class HasChatOwnerLeft(BaseFilter[BaseContext[ChatOwnerLeftMessage]]):
    """У объекта Message заполнено `chat_owner_left`. Гарантирует ChatOwnerLeftMessage."""

    guarantees = ChatOwnerLeftMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.chat_owner_left is not None


class HasChatOwnerChanged(BaseFilter[BaseContext[ChatOwnerChangedMessage]]):
    """У объекта Message заполнено `chat_owner_changed`. Гарантирует ChatOwnerChangedMessage."""

    guarantees = ChatOwnerChangedMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.chat_owner_changed is not None


class HasNewChatTitle(BaseFilter[BaseContext[NewChatTitleMessage]]):
    """У объекта Message заполнено `new_chat_title`. Гарантирует NewChatTitleMessage."""

    guarantees = NewChatTitleMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.new_chat_title is not None


class HasNewChatPhoto(BaseFilter[BaseContext[NewChatPhotoMessage]]):
    """У объекта Message заполнено `new_chat_photo`. Гарантирует NewChatPhotoMessage."""

    guarantees = NewChatPhotoMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.new_chat_photo is not None


class HasDeleteChatPhoto(BaseFilter[BaseContext[DeleteChatPhotoMessage]]):
    """У объекта Message заполнено `delete_chat_photo`. Гарантирует DeleteChatPhotoMessage."""

    guarantees = DeleteChatPhotoMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.delete_chat_photo is not None


class HasGroupChatCreated(BaseFilter[BaseContext[GroupChatCreatedMessage]]):
    """У объекта Message заполнено `group_chat_created`. Гарантирует GroupChatCreatedMessage."""

    guarantees = GroupChatCreatedMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.group_chat_created is not None


class HasSupergroupChatCreated(BaseFilter[BaseContext[SupergroupChatCreatedMessage]]):
    """У объекта Message заполнено `supergroup_chat_created`. Гарантирует SupergroupChatCreatedMessage."""

    guarantees = SupergroupChatCreatedMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.supergroup_chat_created is not None


class HasChannelChatCreated(BaseFilter[BaseContext[ChannelChatCreatedMessage]]):
    """У объекта Message заполнено `channel_chat_created`. Гарантирует ChannelChatCreatedMessage."""

    guarantees = ChannelChatCreatedMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.channel_chat_created is not None


class HasMessageAutoDeleteTimerChanged(BaseFilter[BaseContext[MessageAutoDeleteTimerChangedMessage]]):
    """У объекта Message заполнено `message_auto_delete_timer_changed`. Гарантирует MessageAutoDeleteTimerChangedMessage."""

    guarantees = MessageAutoDeleteTimerChangedMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.message_auto_delete_timer_changed is not None


class HasMigrateToChatId(BaseFilter[BaseContext[MigrateToChatIdMessage]]):
    """У объекта Message заполнено `migrate_to_chat_id`. Гарантирует MigrateToChatIdMessage."""

    guarantees = MigrateToChatIdMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.migrate_to_chat_id is not None


class HasMigrateFromChatId(BaseFilter[BaseContext[MigrateFromChatIdMessage]]):
    """У объекта Message заполнено `migrate_from_chat_id`. Гарантирует MigrateFromChatIdMessage."""

    guarantees = MigrateFromChatIdMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.migrate_from_chat_id is not None


class HasPinnedMessage(BaseFilter[BaseContext[PinnedMessageMessage]]):
    """У объекта Message заполнено `pinned_message`. Гарантирует PinnedMessageMessage."""

    guarantees = PinnedMessageMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.pinned_message is not None


class HasInvoice(BaseFilter[BaseContext[InvoiceMessage]]):
    """У объекта Message заполнено `invoice`. Гарантирует InvoiceMessage."""

    guarantees = InvoiceMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.invoice is not None


class HasSuccessfulPayment(BaseFilter[BaseContext[SuccessfulPaymentMessage]]):
    """У объекта Message заполнено `successful_payment`. Гарантирует SuccessfulPaymentMessage."""

    guarantees = SuccessfulPaymentMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.successful_payment is not None


class HasRefundedPayment(BaseFilter[BaseContext[RefundedPaymentMessage]]):
    """У объекта Message заполнено `refunded_payment`. Гарантирует RefundedPaymentMessage."""

    guarantees = RefundedPaymentMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.refunded_payment is not None


class HasUsersShared(BaseFilter[BaseContext[UsersSharedMessage]]):
    """У объекта Message заполнено `users_shared`. Гарантирует UsersSharedMessage."""

    guarantees = UsersSharedMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.users_shared is not None


class HasChatShared(BaseFilter[BaseContext[ChatSharedMessage]]):
    """У объекта Message заполнено `chat_shared`. Гарантирует ChatSharedMessage."""

    guarantees = ChatSharedMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.chat_shared is not None


class HasGift(BaseFilter[BaseContext[GiftMessage]]):
    """У объекта Message заполнено `gift`. Гарантирует GiftMessage."""

    guarantees = GiftMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.gift is not None


class HasUniqueGift(BaseFilter[BaseContext[UniqueGiftMessage]]):
    """У объекта Message заполнено `unique_gift`. Гарантирует UniqueGiftMessage."""

    guarantees = UniqueGiftMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.unique_gift is not None


class HasGiftUpgradeSent(BaseFilter[BaseContext[GiftUpgradeSentMessage]]):
    """У объекта Message заполнено `gift_upgrade_sent`. Гарантирует GiftUpgradeSentMessage."""

    guarantees = GiftUpgradeSentMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.gift_upgrade_sent is not None


class HasConnectedWebsite(BaseFilter[BaseContext[ConnectedWebsiteMessage]]):
    """У объекта Message заполнено `connected_website`. Гарантирует ConnectedWebsiteMessage."""

    guarantees = ConnectedWebsiteMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.connected_website is not None


class HasWriteAccessAllowed(BaseFilter[BaseContext[WriteAccessAllowedMessage]]):
    """У объекта Message заполнено `write_access_allowed`. Гарантирует WriteAccessAllowedMessage."""

    guarantees = WriteAccessAllowedMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.write_access_allowed is not None


class HasPassportData(BaseFilter[BaseContext[PassportDataMessage]]):
    """У объекта Message заполнено `passport_data`. Гарантирует PassportDataMessage."""

    guarantees = PassportDataMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.passport_data is not None


class HasProximityAlertTriggered(BaseFilter[BaseContext[ProximityAlertTriggeredMessage]]):
    """У объекта Message заполнено `proximity_alert_triggered`. Гарантирует ProximityAlertTriggeredMessage."""

    guarantees = ProximityAlertTriggeredMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.proximity_alert_triggered is not None


class HasBoostAdded(BaseFilter[BaseContext[BoostAddedMessage]]):
    """У объекта Message заполнено `boost_added`. Гарантирует BoostAddedMessage."""

    guarantees = BoostAddedMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.boost_added is not None


class HasChatBackgroundSet(BaseFilter[BaseContext[ChatBackgroundSetMessage]]):
    """У объекта Message заполнено `chat_background_set`. Гарантирует ChatBackgroundSetMessage."""

    guarantees = ChatBackgroundSetMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.chat_background_set is not None


class HasChecklistTasksDone(BaseFilter[BaseContext[ChecklistTasksDoneMessage]]):
    """У объекта Message заполнено `checklist_tasks_done`. Гарантирует ChecklistTasksDoneMessage."""

    guarantees = ChecklistTasksDoneMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.checklist_tasks_done is not None


class HasChecklistTasksAdded(BaseFilter[BaseContext[ChecklistTasksAddedMessage]]):
    """У объекта Message заполнено `checklist_tasks_added`. Гарантирует ChecklistTasksAddedMessage."""

    guarantees = ChecklistTasksAddedMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.checklist_tasks_added is not None


class HasCommunityChatAdded(BaseFilter[BaseContext[CommunityChatAddedMessage]]):
    """У объекта Message заполнено `community_chat_added`. Гарантирует CommunityChatAddedMessage."""

    guarantees = CommunityChatAddedMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.community_chat_added is not None


class HasCommunityChatJoined(BaseFilter[BaseContext[CommunityChatJoinedMessage]]):
    """У объекта Message заполнено `community_chat_joined`. Гарантирует CommunityChatJoinedMessage."""

    guarantees = CommunityChatJoinedMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.community_chat_joined is not None


class HasCommunityChatRemoved(BaseFilter[BaseContext[CommunityChatRemovedMessage]]):
    """У объекта Message заполнено `community_chat_removed`. Гарантирует CommunityChatRemovedMessage."""

    guarantees = CommunityChatRemovedMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.community_chat_removed is not None


class HasDirectMessagePriceChanged(BaseFilter[BaseContext[DirectMessagePriceChangedMessage]]):
    """У объекта Message заполнено `direct_message_price_changed`. Гарантирует DirectMessagePriceChangedMessage."""

    guarantees = DirectMessagePriceChangedMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.direct_message_price_changed is not None


class HasForumTopicCreated(BaseFilter[BaseContext[ForumTopicCreatedMessage]]):
    """У объекта Message заполнено `forum_topic_created`. Гарантирует ForumTopicCreatedMessage."""

    guarantees = ForumTopicCreatedMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.forum_topic_created is not None


class HasForumTopicEdited(BaseFilter[BaseContext[ForumTopicEditedMessage]]):
    """У объекта Message заполнено `forum_topic_edited`. Гарантирует ForumTopicEditedMessage."""

    guarantees = ForumTopicEditedMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.forum_topic_edited is not None


class HasForumTopicClosed(BaseFilter[BaseContext[ForumTopicClosedMessage]]):
    """У объекта Message заполнено `forum_topic_closed`. Гарантирует ForumTopicClosedMessage."""

    guarantees = ForumTopicClosedMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.forum_topic_closed is not None


class HasForumTopicReopened(BaseFilter[BaseContext[ForumTopicReopenedMessage]]):
    """У объекта Message заполнено `forum_topic_reopened`. Гарантирует ForumTopicReopenedMessage."""

    guarantees = ForumTopicReopenedMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.forum_topic_reopened is not None


class HasGeneralForumTopicHidden(BaseFilter[BaseContext[GeneralForumTopicHiddenMessage]]):
    """У объекта Message заполнено `general_forum_topic_hidden`. Гарантирует GeneralForumTopicHiddenMessage."""

    guarantees = GeneralForumTopicHiddenMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.general_forum_topic_hidden is not None


class HasGeneralForumTopicUnhidden(BaseFilter[BaseContext[GeneralForumTopicUnhiddenMessage]]):
    """У объекта Message заполнено `general_forum_topic_unhidden`. Гарантирует GeneralForumTopicUnhiddenMessage."""

    guarantees = GeneralForumTopicUnhiddenMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.general_forum_topic_unhidden is not None


class HasGiveawayCreated(BaseFilter[BaseContext[GiveawayCreatedMessage]]):
    """У объекта Message заполнено `giveaway_created`. Гарантирует GiveawayCreatedMessage."""

    guarantees = GiveawayCreatedMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.giveaway_created is not None


class HasGiveaway(BaseFilter[BaseContext[GiveawayMessage]]):
    """У объекта Message заполнено `giveaway`. Гарантирует GiveawayMessage."""

    guarantees = GiveawayMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.giveaway is not None


class HasGiveawayWinners(BaseFilter[BaseContext[GiveawayWinnersMessage]]):
    """У объекта Message заполнено `giveaway_winners`. Гарантирует GiveawayWinnersMessage."""

    guarantees = GiveawayWinnersMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.giveaway_winners is not None


class HasGiveawayCompleted(BaseFilter[BaseContext[GiveawayCompletedMessage]]):
    """У объекта Message заполнено `giveaway_completed`. Гарантирует GiveawayCompletedMessage."""

    guarantees = GiveawayCompletedMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.giveaway_completed is not None


class HasManagedBotCreated(BaseFilter[BaseContext[ManagedBotCreatedMessage]]):
    """У объекта Message заполнено `managed_bot_created`. Гарантирует ManagedBotCreatedMessage."""

    guarantees = ManagedBotCreatedMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.managed_bot_created is not None


class HasPaidMessagePriceChanged(BaseFilter[BaseContext[PaidMessagePriceChangedMessage]]):
    """У объекта Message заполнено `paid_message_price_changed`. Гарантирует PaidMessagePriceChangedMessage."""

    guarantees = PaidMessagePriceChangedMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.paid_message_price_changed is not None


class HasPollOptionAdded(BaseFilter[BaseContext[PollOptionAddedMessage]]):
    """У объекта Message заполнено `poll_option_added`. Гарантирует PollOptionAddedMessage."""

    guarantees = PollOptionAddedMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.poll_option_added is not None


class HasPollOptionDeleted(BaseFilter[BaseContext[PollOptionDeletedMessage]]):
    """У объекта Message заполнено `poll_option_deleted`. Гарантирует PollOptionDeletedMessage."""

    guarantees = PollOptionDeletedMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.poll_option_deleted is not None


class HasSuggestedPostApproved(BaseFilter[BaseContext[SuggestedPostApprovedMessage]]):
    """У объекта Message заполнено `suggested_post_approved`. Гарантирует SuggestedPostApprovedMessage."""

    guarantees = SuggestedPostApprovedMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.suggested_post_approved is not None


class HasSuggestedPostApprovalFailed(BaseFilter[BaseContext[SuggestedPostApprovalFailedMessage]]):
    """У объекта Message заполнено `suggested_post_approval_failed`. Гарантирует SuggestedPostApprovalFailedMessage."""

    guarantees = SuggestedPostApprovalFailedMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.suggested_post_approval_failed is not None


class HasSuggestedPostDeclined(BaseFilter[BaseContext[SuggestedPostDeclinedMessage]]):
    """У объекта Message заполнено `suggested_post_declined`. Гарантирует SuggestedPostDeclinedMessage."""

    guarantees = SuggestedPostDeclinedMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.suggested_post_declined is not None


class HasSuggestedPostPaid(BaseFilter[BaseContext[SuggestedPostPaidMessage]]):
    """У объекта Message заполнено `suggested_post_paid`. Гарантирует SuggestedPostPaidMessage."""

    guarantees = SuggestedPostPaidMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.suggested_post_paid is not None


class HasSuggestedPostRefunded(BaseFilter[BaseContext[SuggestedPostRefundedMessage]]):
    """У объекта Message заполнено `suggested_post_refunded`. Гарантирует SuggestedPostRefundedMessage."""

    guarantees = SuggestedPostRefundedMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.suggested_post_refunded is not None


class HasVideoChatScheduled(BaseFilter[BaseContext[VideoChatScheduledMessage]]):
    """У объекта Message заполнено `video_chat_scheduled`. Гарантирует VideoChatScheduledMessage."""

    guarantees = VideoChatScheduledMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.video_chat_scheduled is not None


class HasVideoChatStarted(BaseFilter[BaseContext[VideoChatStartedMessage]]):
    """У объекта Message заполнено `video_chat_started`. Гарантирует VideoChatStartedMessage."""

    guarantees = VideoChatStartedMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.video_chat_started is not None


class HasVideoChatEnded(BaseFilter[BaseContext[VideoChatEndedMessage]]):
    """У объекта Message заполнено `video_chat_ended`. Гарантирует VideoChatEndedMessage."""

    guarantees = VideoChatEndedMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.video_chat_ended is not None


class HasVideoChatParticipantsInvited(BaseFilter[BaseContext[VideoChatParticipantsInvitedMessage]]):
    """У объекта Message заполнено `video_chat_participants_invited`. Гарантирует VideoChatParticipantsInvitedMessage."""

    guarantees = VideoChatParticipantsInvitedMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.video_chat_participants_invited is not None


class HasWebAppData(BaseFilter[BaseContext[WebAppDataMessage]]):
    """У объекта Message заполнено `web_app_data`. Гарантирует WebAppDataMessage."""

    guarantees = WebAppDataMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.web_app_data is not None


class HasReplyMarkup(BaseFilter[BaseContext[ReplyMarkupMessage]]):
    """У объекта Message заполнено `reply_markup`. Гарантирует ReplyMarkupMessage."""

    guarantees = ReplyMarkupMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Message) and event.reply_markup is not None


class HasRightsBusinessConnection(BaseFilter[BaseContext[RightsBusinessConnection]]):
    """У объекта BusinessConnection заполнено `rights`. Гарантирует RightsBusinessConnection."""

    guarantees = RightsBusinessConnection

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, BusinessConnection) and event.rights is not None


class HasUserMessageReactionUpdated(BaseFilter[BaseContext[UserMessageReactionUpdated]]):
    """У объекта MessageReactionUpdated заполнено `user`. Гарантирует UserMessageReactionUpdated."""

    guarantees = UserMessageReactionUpdated

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, MessageReactionUpdated) and event.user is not None


class HasActorChatMessageReactionUpdated(BaseFilter[BaseContext[ActorChatMessageReactionUpdated]]):
    """У объекта MessageReactionUpdated заполнено `actor_chat`. Гарантирует ActorChatMessageReactionUpdated."""

    guarantees = ActorChatMessageReactionUpdated

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, MessageReactionUpdated) and event.actor_chat is not None


class HasChatTypeInlineQuery(BaseFilter[BaseContext[ChatTypeInlineQuery]]):
    """У объекта InlineQuery заполнено `chat_type`. Гарантирует ChatTypeInlineQuery."""

    guarantees = ChatTypeInlineQuery

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, InlineQuery) and event.chat_type is not None


class HasLocationInlineQuery(BaseFilter[BaseContext[LocationInlineQuery]]):
    """У объекта InlineQuery заполнено `location`. Гарантирует LocationInlineQuery."""

    guarantees = LocationInlineQuery

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, InlineQuery) and event.location is not None


class HasLocationChosenInlineResult(BaseFilter[BaseContext[LocationChosenInlineResult]]):
    """У объекта ChosenInlineResult заполнено `location`. Гарантирует LocationChosenInlineResult."""

    guarantees = LocationChosenInlineResult

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, ChosenInlineResult) and event.location is not None


class HasInlineMessageIdChosenInlineResult(BaseFilter[BaseContext[InlineMessageIdChosenInlineResult]]):
    """У объекта ChosenInlineResult заполнено `inline_message_id`. Гарантирует InlineMessageIdChosenInlineResult."""

    guarantees = InlineMessageIdChosenInlineResult

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, ChosenInlineResult) and event.inline_message_id is not None


class HasMessageCallbackQuery(BaseFilter[BaseContext[MessageCallbackQuery]]):
    """У объекта CallbackQuery заполнено `message`. Гарантирует MessageCallbackQuery."""

    guarantees = MessageCallbackQuery

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, CallbackQuery) and event.message is not None


class HasInlineMessageIdCallbackQuery(BaseFilter[BaseContext[InlineMessageIdCallbackQuery]]):
    """У объекта CallbackQuery заполнено `inline_message_id`. Гарантирует InlineMessageIdCallbackQuery."""

    guarantees = InlineMessageIdCallbackQuery

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, CallbackQuery) and event.inline_message_id is not None


class HasDataCallbackQuery(BaseFilter[BaseContext[DataCallbackQuery]]):
    """У объекта CallbackQuery заполнено `data`. Гарантирует DataCallbackQuery."""

    guarantees = DataCallbackQuery

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, CallbackQuery) and event.data is not None


class HasGameShortNameCallbackQuery(BaseFilter[BaseContext[GameShortNameCallbackQuery]]):
    """У объекта CallbackQuery заполнено `game_short_name`. Гарантирует GameShortNameCallbackQuery."""

    guarantees = GameShortNameCallbackQuery

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, CallbackQuery) and event.game_short_name is not None


class HasShippingOptionIdPreCheckoutQuery(BaseFilter[BaseContext[ShippingOptionIdPreCheckoutQuery]]):
    """У объекта PreCheckoutQuery заполнено `shipping_option_id`. Гарантирует ShippingOptionIdPreCheckoutQuery."""

    guarantees = ShippingOptionIdPreCheckoutQuery

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, PreCheckoutQuery) and event.shipping_option_id is not None


class HasOrderInfoPreCheckoutQuery(BaseFilter[BaseContext[OrderInfoPreCheckoutQuery]]):
    """У объекта PreCheckoutQuery заполнено `order_info`. Гарантирует OrderInfoPreCheckoutQuery."""

    guarantees = OrderInfoPreCheckoutQuery

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, PreCheckoutQuery) and event.order_info is not None


class HasQuestionEntitiesPoll(BaseFilter[BaseContext[QuestionEntitiesPoll]]):
    """У объекта Poll заполнено `question_entities`. Гарантирует QuestionEntitiesPoll."""

    guarantees = QuestionEntitiesPoll

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Poll) and event.question_entities is not None


class HasCountryCodesPoll(BaseFilter[BaseContext[CountryCodesPoll]]):
    """У объекта Poll заполнено `country_codes`. Гарантирует CountryCodesPoll."""

    guarantees = CountryCodesPoll

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Poll) and event.country_codes is not None


class HasCorrectOptionIdsPoll(BaseFilter[BaseContext[CorrectOptionIdsPoll]]):
    """У объекта Poll заполнено `correct_option_ids`. Гарантирует CorrectOptionIdsPoll."""

    guarantees = CorrectOptionIdsPoll

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Poll) and event.correct_option_ids is not None


class HasExplanationPoll(BaseFilter[BaseContext[ExplanationPoll]]):
    """У объекта Poll заполнено `explanation`. Гарантирует ExplanationPoll."""

    guarantees = ExplanationPoll

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Poll) and event.explanation is not None


class HasExplanationEntitiesPoll(BaseFilter[BaseContext[ExplanationEntitiesPoll]]):
    """У объекта Poll заполнено `explanation_entities`. Гарантирует ExplanationEntitiesPoll."""

    guarantees = ExplanationEntitiesPoll

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Poll) and event.explanation_entities is not None


class HasExplanationMediaPoll(BaseFilter[BaseContext[ExplanationMediaPoll]]):
    """У объекта Poll заполнено `explanation_media`. Гарантирует ExplanationMediaPoll."""

    guarantees = ExplanationMediaPoll

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Poll) and event.explanation_media is not None


class HasOpenPeriodPoll(BaseFilter[BaseContext[OpenPeriodPoll]]):
    """У объекта Poll заполнено `open_period`. Гарантирует OpenPeriodPoll."""

    guarantees = OpenPeriodPoll

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Poll) and event.open_period is not None


class HasCloseDatePoll(BaseFilter[BaseContext[CloseDatePoll]]):
    """У объекта Poll заполнено `close_date`. Гарантирует CloseDatePoll."""

    guarantees = CloseDatePoll

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Poll) and event.close_date is not None


class HasDescriptionPoll(BaseFilter[BaseContext[DescriptionPoll]]):
    """У объекта Poll заполнено `description`. Гарантирует DescriptionPoll."""

    guarantees = DescriptionPoll

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Poll) and event.description is not None


class HasDescriptionEntitiesPoll(BaseFilter[BaseContext[DescriptionEntitiesPoll]]):
    """У объекта Poll заполнено `description_entities`. Гарантирует DescriptionEntitiesPoll."""

    guarantees = DescriptionEntitiesPoll

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Poll) and event.description_entities is not None


class HasMediaPoll(BaseFilter[BaseContext[MediaPoll]]):
    """У объекта Poll заполнено `media`. Гарантирует MediaPoll."""

    guarantees = MediaPoll

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, Poll) and event.media is not None


class HasVoterChatPollAnswer(BaseFilter[BaseContext[VoterChatPollAnswer]]):
    """У объекта PollAnswer заполнено `voter_chat`. Гарантирует VoterChatPollAnswer."""

    guarantees = VoterChatPollAnswer

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, PollAnswer) and event.voter_chat is not None


class HasUserPollAnswer(BaseFilter[BaseContext[UserPollAnswer]]):
    """У объекта PollAnswer заполнено `user`. Гарантирует UserPollAnswer."""

    guarantees = UserPollAnswer

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, PollAnswer) and event.user is not None


class HasInviteLinkChatMemberUpdated(BaseFilter[BaseContext[InviteLinkChatMemberUpdated]]):
    """У объекта ChatMemberUpdated заполнено `invite_link`. Гарантирует InviteLinkChatMemberUpdated."""

    guarantees = InviteLinkChatMemberUpdated

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, ChatMemberUpdated) and event.invite_link is not None


class HasViaJoinRequestChatMemberUpdated(BaseFilter[BaseContext[ViaJoinRequestChatMemberUpdated]]):
    """У объекта ChatMemberUpdated заполнено `via_join_request`. Гарантирует ViaJoinRequestChatMemberUpdated."""

    guarantees = ViaJoinRequestChatMemberUpdated

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, ChatMemberUpdated) and event.via_join_request is not None


class HasViaChatFolderInviteLinkChatMemberUpdated(BaseFilter[BaseContext[ViaChatFolderInviteLinkChatMemberUpdated]]):
    """У объекта ChatMemberUpdated заполнено `via_chat_folder_invite_link`. Гарантирует ViaChatFolderInviteLinkChatMemberUpdated."""

    guarantees = ViaChatFolderInviteLinkChatMemberUpdated

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, ChatMemberUpdated) and event.via_chat_folder_invite_link is not None


class HasBioChatJoinRequest(BaseFilter[BaseContext[BioChatJoinRequest]]):
    """У объекта ChatJoinRequest заполнено `bio`. Гарантирует BioChatJoinRequest."""

    guarantees = BioChatJoinRequest

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, ChatJoinRequest) and event.bio is not None


class HasInviteLinkChatJoinRequest(BaseFilter[BaseContext[InviteLinkChatJoinRequest]]):
    """У объекта ChatJoinRequest заполнено `invite_link`. Гарантирует InviteLinkChatJoinRequest."""

    guarantees = InviteLinkChatJoinRequest

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, ChatJoinRequest) and event.invite_link is not None


class HasQueryIdChatJoinRequest(BaseFilter[BaseContext[QueryIdChatJoinRequest]]):
    """У объекта ChatJoinRequest заполнено `query_id`. Гарантирует QueryIdChatJoinRequest."""

    guarantees = QueryIdChatJoinRequest

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, ChatJoinRequest) and event.query_id is not None


class HasMessageThreadIdMessageGenerationStopped(BaseFilter[BaseContext[MessageThreadIdMessageGenerationStopped]]):
    """У объекта MessageGenerationStopped заполнено `message_thread_id`. Гарантирует MessageThreadIdMessageGenerationStopped."""

    guarantees = MessageThreadIdMessageGenerationStopped

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        return isinstance(event, MessageGenerationStopped) and event.message_thread_id is not None


class HasReplyUser(BaseFilter[BaseContext[ReplyUserMessage]]):
    """У ответа `reply_to_message` заполнено `user`. Гарантирует ReplyUserMessage."""

    guarantees = ReplyUserMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        reply = event.reply_to_message if isinstance(event, Message) else None
        return reply is not None and reply.user is not None


class HasReplyText(BaseFilter[BaseContext[ReplyTextMessage]]):
    """У ответа `reply_to_message` заполнено `text`. Гарантирует ReplyTextMessage."""

    guarantees = ReplyTextMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        reply = event.reply_to_message if isinstance(event, Message) else None
        return reply is not None and reply.text is not None


class HasReplyEntities(BaseFilter[BaseContext[ReplyEntitiesMessage]]):
    """У ответа `reply_to_message` заполнено `entities`. Гарантирует ReplyEntitiesMessage."""

    guarantees = ReplyEntitiesMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        reply = event.reply_to_message if isinstance(event, Message) else None
        return reply is not None and reply.entities is not None


class HasReplyCaption(BaseFilter[BaseContext[ReplyCaptionMessage]]):
    """У ответа `reply_to_message` заполнено `caption`. Гарантирует ReplyCaptionMessage."""

    guarantees = ReplyCaptionMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        reply = event.reply_to_message if isinstance(event, Message) else None
        return reply is not None and reply.caption is not None


class HasReplyCaptionEntities(BaseFilter[BaseContext[ReplyCaptionEntitiesMessage]]):
    """У ответа `reply_to_message` заполнено `caption_entities`. Гарантирует ReplyCaptionEntitiesMessage."""

    guarantees = ReplyCaptionEntitiesMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        reply = event.reply_to_message if isinstance(event, Message) else None
        return reply is not None and reply.caption_entities is not None


class HasReplyPhoto(BaseFilter[BaseContext[ReplyPhotoMessage]]):
    """У ответа `reply_to_message` заполнено `photo`. Гарантирует ReplyPhotoMessage."""

    guarantees = ReplyPhotoMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        reply = event.reply_to_message if isinstance(event, Message) else None
        return reply is not None and reply.photo is not None


class HasReplyAnimation(BaseFilter[BaseContext[ReplyAnimationMessage]]):
    """У ответа `reply_to_message` заполнено `animation`. Гарантирует ReplyAnimationMessage."""

    guarantees = ReplyAnimationMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        reply = event.reply_to_message if isinstance(event, Message) else None
        return reply is not None and reply.animation is not None


class HasReplyAudio(BaseFilter[BaseContext[ReplyAudioMessage]]):
    """У ответа `reply_to_message` заполнено `audio`. Гарантирует ReplyAudioMessage."""

    guarantees = ReplyAudioMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        reply = event.reply_to_message if isinstance(event, Message) else None
        return reply is not None and reply.audio is not None


class HasReplyDocument(BaseFilter[BaseContext[ReplyDocumentMessage]]):
    """У ответа `reply_to_message` заполнено `document`. Гарантирует ReplyDocumentMessage."""

    guarantees = ReplyDocumentMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        reply = event.reply_to_message if isinstance(event, Message) else None
        return reply is not None and reply.document is not None


class HasReplySticker(BaseFilter[BaseContext[ReplyStickerMessage]]):
    """У ответа `reply_to_message` заполнено `sticker`. Гарантирует ReplyStickerMessage."""

    guarantees = ReplyStickerMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        reply = event.reply_to_message if isinstance(event, Message) else None
        return reply is not None and reply.sticker is not None


class HasReplyVideo(BaseFilter[BaseContext[ReplyVideoMessage]]):
    """У ответа `reply_to_message` заполнено `video`. Гарантирует ReplyVideoMessage."""

    guarantees = ReplyVideoMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        reply = event.reply_to_message if isinstance(event, Message) else None
        return reply is not None and reply.video is not None


class HasReplyVideoNote(BaseFilter[BaseContext[ReplyVideoNoteMessage]]):
    """У ответа `reply_to_message` заполнено `video_note`. Гарантирует ReplyVideoNoteMessage."""

    guarantees = ReplyVideoNoteMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        reply = event.reply_to_message if isinstance(event, Message) else None
        return reply is not None and reply.video_note is not None


class HasReplyVoice(BaseFilter[BaseContext[ReplyVoiceMessage]]):
    """У ответа `reply_to_message` заполнено `voice`. Гарантирует ReplyVoiceMessage."""

    guarantees = ReplyVoiceMessage

    async def check(self, ctx: BaseContext[Any]) -> bool:
        event = ctx.event
        reply = event.reply_to_message if isinstance(event, Message) else None
        return reply is not None and reply.voice is not None


__all__ = [
    "HasActorChatMessageReactionUpdated",
    "HasAnimation",
    "HasAudio",
    "HasAuthorSignature",
    "HasBioChatJoinRequest",
    "HasBoostAdded",
    "HasBusinessConnectionId",
    "HasCaption",
    "HasCaptionEntities",
    "HasChannelChatCreated",
    "HasChatBackgroundSet",
    "HasChatOwnerChanged",
    "HasChatOwnerLeft",
    "HasChatShared",
    "HasChatTypeInlineQuery",
    "HasChecklist",
    "HasChecklistTasksAdded",
    "HasChecklistTasksDone",
    "HasCloseDatePoll",
    "HasCommunityChatAdded",
    "HasCommunityChatJoined",
    "HasCommunityChatRemoved",
    "HasConnectedWebsite",
    "HasContact",
    "HasCorrectOptionIdsPoll",
    "HasCountryCodesPoll",
    "HasDataCallbackQuery",
    "HasDeleteChatPhoto",
    "HasDescriptionEntitiesPoll",
    "HasDescriptionPoll",
    "HasDice",
    "HasDirectMessagePriceChanged",
    "HasDirectMessagesTopic",
    "HasDocument",
    "HasEditDate",
    "HasEffectId",
    "HasEntities",
    "HasEphemeralMessageId",
    "HasExplanationEntitiesPoll",
    "HasExplanationMediaPoll",
    "HasExplanationPoll",
    "HasExternalReply",
    "HasForumTopicClosed",
    "HasForumTopicCreated",
    "HasForumTopicEdited",
    "HasForumTopicReopened",
    "HasForwardOrigin",
    "HasGame",
    "HasGameShortNameCallbackQuery",
    "HasGeneralForumTopicHidden",
    "HasGeneralForumTopicUnhidden",
    "HasGift",
    "HasGiftUpgradeSent",
    "HasGiveaway",
    "HasGiveawayCompleted",
    "HasGiveawayCreated",
    "HasGiveawayWinners",
    "HasGroupChatCreated",
    "HasGuestBotCallerChat",
    "HasGuestBotCallerUser",
    "HasGuestQueryId",
    "HasHasMediaSpoiler",
    "HasHasProtectedContent",
    "HasInlineMessageIdCallbackQuery",
    "HasInlineMessageIdChosenInlineResult",
    "HasInviteLinkChatJoinRequest",
    "HasInviteLinkChatMemberUpdated",
    "HasInvoice",
    "HasIsAutomaticForward",
    "HasIsFromOffline",
    "HasIsPaidPost",
    "HasIsTopicMessage",
    "HasLeftChatMember",
    "HasLinkPreviewOptions",
    "HasLivePhoto",
    "HasLocation",
    "HasLocationChosenInlineResult",
    "HasLocationInlineQuery",
    "HasManagedBotCreated",
    "HasMediaGroupId",
    "HasMediaPoll",
    "HasMessageAutoDeleteTimerChanged",
    "HasMessageCallbackQuery",
    "HasMessageThreadId",
    "HasMessageThreadIdMessageGenerationStopped",
    "HasMigrateFromChatId",
    "HasMigrateToChatId",
    "HasNewChatMembers",
    "HasNewChatPhoto",
    "HasNewChatTitle",
    "HasOpenPeriodPoll",
    "HasOrderInfoPreCheckoutQuery",
    "HasPaidMedia",
    "HasPaidMessagePriceChanged",
    "HasPaidStarCount",
    "HasPassportData",
    "HasPhoto",
    "HasPinnedMessage",
    "HasPoll",
    "HasPollOptionAdded",
    "HasPollOptionDeleted",
    "HasProximityAlertTriggered",
    "HasQueryIdChatJoinRequest",
    "HasQuestionEntitiesPoll",
    "HasQuote",
    "HasReceiverUser",
    "HasRefundedPayment",
    "HasReplyAnimation",
    "HasReplyAudio",
    "HasReplyCaption",
    "HasReplyCaptionEntities",
    "HasReplyDocument",
    "HasReplyEntities",
    "HasReplyMarkup",
    "HasReplyPhoto",
    "HasReplySticker",
    "HasReplyText",
    "HasReplyToChecklistTaskId",
    "HasReplyToMessage",
    "HasReplyToPollOptionId",
    "HasReplyToStory",
    "HasReplyUser",
    "HasReplyVideo",
    "HasReplyVideoNote",
    "HasReplyVoice",
    "HasRichMessage",
    "HasRightsBusinessConnection",
    "HasSenderBoostCount",
    "HasSenderBusinessBot",
    "HasSenderChat",
    "HasSenderTag",
    "HasShippingOptionIdPreCheckoutQuery",
    "HasShowCaptionAboveMedia",
    "HasSticker",
    "HasStory",
    "HasSuccessfulPayment",
    "HasSuggestedPostApprovalFailed",
    "HasSuggestedPostApproved",
    "HasSuggestedPostDeclined",
    "HasSuggestedPostInfo",
    "HasSuggestedPostPaid",
    "HasSuggestedPostRefunded",
    "HasSupergroupChatCreated",
    "HasText",
    "HasUniqueGift",
    "HasUser",
    "HasUserMessageReactionUpdated",
    "HasUserPollAnswer",
    "HasUsersShared",
    "HasVenue",
    "HasViaBot",
    "HasViaChatFolderInviteLinkChatMemberUpdated",
    "HasViaJoinRequestChatMemberUpdated",
    "HasVideo",
    "HasVideoChatEnded",
    "HasVideoChatParticipantsInvited",
    "HasVideoChatScheduled",
    "HasVideoChatStarted",
    "HasVideoNote",
    "HasVoice",
    "HasVoterChatPollAnswer",
    "HasWebAppData",
    "HasWriteAccessAllowed",
]
