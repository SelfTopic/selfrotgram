# АВТОГЕНЕРАЦИЯ: scripts/generate_types.py, Telegram Bot API 10.3, August 24, 2026.
# Руками не править — обновилась спека, перегенерировать.
# ruff: noqa
from __future__ import annotations

from typing import List, Optional, Union

from ..types import *
from .accessors import TEvent, _TCallbackQuery, _TInlineQuery, _TPreCheckoutQuery, _TShippingQuery
from .helpers import ContextHelpers


class ContextMethods(ContextHelpers[TEvent]):
    """
    Ярлыки методов Bot: то же, что bot.<метод>(...), но чат, сообщение и id
    запроса берутся из текущего апдейта. answer_* пишет в чат, reply_* ещё и
    цитирует сообщение. Для другого чата: ctx.bot.<метод>(...).
    """

    async def answer_message(
        self,
        text: str,
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        parse_mode: Optional[str] = None,
        entities: Optional[List[MessageEntity]] = None,
        link_preview_options: Optional[LinkPreviewOptions] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_message(), но чат берётся из апдейта.
        
        Use this method to send text messages. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendmessage
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
            message_thread_id: Unique identifier for the target message thread (topic) of a forum; for forum supergroups and private chats of bots with forum topic mode enabled only
            direct_messages_topic_id: Identifier of the direct messages topic to which the message will be sent; required if the message is sent to a direct messages chat
            ephemeral_message_parameters: A JSON-serialized object containing the parameters of the ephemeral message to send
            text: Text of the message to be sent, 1-4096 characters after entities parsing
            parse_mode: Mode for parsing entities in the message text. See formatting options for more details.
            entities: A JSON-serialized list of special entities that appear in message text, which can be specified instead of parse_mode
            link_preview_options: Link preview generation options for the message
            disable_notification: Sends the message silently. Users will receive a notification with no sound.
            protect_content: Protects the contents of the sent message from forwarding and saving
            allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance.
            message_effect_id: Unique identifier of the message effect to be added to the message; for private chats only
            suggested_post_parameters: A JSON-serialized object containing the parameters of the suggested post to send; for direct messages chats only. If the message is sent as a reply to another suggested post, then that suggested post is automatically declined.
            reply_parameters: Description of the message to reply to
            reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user.
        """
        return await self.bot.send_message(
            business_connection_id=self._or_default("business_connection_id", business_connection_id),
            chat_id=self.chat_id,
            message_thread_id=self._or_default("message_thread_id", message_thread_id),
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            text=text,
            parse_mode=parse_mode,
            entities=entities,
            link_preview_options=link_preview_options,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def reply_message(
        self,
        text: str,
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        parse_mode: Optional[str] = None,
        entities: Optional[List[MessageEntity]] = None,
        link_preview_options: Optional[LinkPreviewOptions] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_message(), но чат берётся из апдейта, сообщение цитирует сообщение апдейта.
        
        Use this method to send text messages. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendmessage
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
            message_thread_id: Unique identifier for the target message thread (topic) of a forum; for forum supergroups and private chats of bots with forum topic mode enabled only
            direct_messages_topic_id: Identifier of the direct messages topic to which the message will be sent; required if the message is sent to a direct messages chat
            ephemeral_message_parameters: A JSON-serialized object containing the parameters of the ephemeral message to send
            text: Text of the message to be sent, 1-4096 characters after entities parsing
            parse_mode: Mode for parsing entities in the message text. See formatting options for more details.
            entities: A JSON-serialized list of special entities that appear in message text, which can be specified instead of parse_mode
            link_preview_options: Link preview generation options for the message
            disable_notification: Sends the message silently. Users will receive a notification with no sound.
            protect_content: Protects the contents of the sent message from forwarding and saving
            allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance.
            message_effect_id: Unique identifier of the message effect to be added to the message; for private chats only
            suggested_post_parameters: A JSON-serialized object containing the parameters of the suggested post to send; for direct messages chats only. If the message is sent as a reply to another suggested post, then that suggested post is automatically declined.
            reply_parameters: Description of the message to reply to
            reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user.
        """
        return await self.bot.send_message(
            business_connection_id=self._or_default("business_connection_id", business_connection_id),
            chat_id=self.chat_id,
            message_thread_id=self._or_default("message_thread_id", message_thread_id),
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            text=text,
            parse_mode=parse_mode,
            entities=entities,
            link_preview_options=link_preview_options,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters if reply_parameters is not None else self._reply_parameters(),
            reply_markup=reply_markup,
        )

    async def forward_message(
        self,
        chat_id: Union[int, str],
        *,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        video_start_timestamp: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        message_id: Optional[int] = None,
    ) -> Message:
        """Как bot.forward_message(), но from_chat_id и message_id берутся из апдейта.
        
        Use this method to forward messages of any kind. Service messages and messages with protected content can't be forwarded. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#forwardmessage
        
        Args:
            chat_id: Unique identifier for the target chat or username of the target bot, supergroup or channel in the format @username
            message_thread_id: Unique identifier for the target message thread (topic) of a forum; for forum supergroups and private chats of bots with forum topic mode enabled only
            direct_messages_topic_id: Identifier of the direct messages topic to which the message will be forwarded; required if the message is forwarded to a direct messages chat
            video_start_timestamp: New start timestamp for the forwarded video in the message
            disable_notification: Sends the message silently. Users will receive a notification with no sound.
            protect_content: Protects the contents of the forwarded message from forwarding and saving
            message_effect_id: Unique identifier of the message effect to be added to the message; only available when forwarding to private chats
            suggested_post_parameters: A JSON-serialized object containing the parameters of the suggested post to send; for direct messages chats only
            message_id: Message identifier in the chat specified in from_chat_id
        """
        return await self.bot.forward_message(
            chat_id=chat_id,
            message_thread_id=message_thread_id,
            direct_messages_topic_id=direct_messages_topic_id,
            from_chat_id=self.chat_id,
            video_start_timestamp=video_start_timestamp,
            disable_notification=disable_notification,
            protect_content=protect_content,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            message_id=message_id if message_id is not None else self._require_message_id(),
        )

    async def forward_messages(
        self,
        chat_id: Union[int, str],
        message_ids: List[int],
        *,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
    ) -> List[MessageId]:
        """Как bot.forward_messages(), но from_chat_id и message_id берутся из апдейта.
        
        Use this method to forward multiple messages of any kind. If some of the specified messages can't be found or forwarded, they are skipped. Service messages and messages with protected content can't be forwarded. Album grouping is kept for forwarded messages. On success, an Array of MessageId of the sent messages is returned.
        
        https://core.telegram.org/bots/api#forwardmessages
        
        Args:
            chat_id: Unique identifier for the target chat or username of the target bot, supergroup or channel in the format @username
            message_thread_id: Unique identifier for the target message thread (topic) of a forum; for forum supergroups and private chats of bots with forum topic mode enabled only
            direct_messages_topic_id: Identifier of the direct messages topic to which the messages will be forwarded; required if the messages are forwarded to a direct messages chat
            message_ids: A JSON-serialized list of 1-100 identifiers of messages in the chat from_chat_id to forward. The identifiers must be specified in a strictly increasing order.
            disable_notification: Sends the messages silently. Users will receive a notification with no sound.
            protect_content: Protects the contents of the forwarded messages from forwarding and saving
        """
        return await self.bot.forward_messages(
            chat_id=chat_id,
            message_thread_id=message_thread_id,
            direct_messages_topic_id=direct_messages_topic_id,
            from_chat_id=self.chat_id,
            message_ids=message_ids,
            disable_notification=disable_notification,
            protect_content=protect_content,
        )

    async def copy_message(
        self,
        chat_id: Union[int, str],
        *,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        message_id: Optional[int] = None,
        video_start_timestamp: Optional[int] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        show_caption_above_media: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> MessageId:
        """Как bot.copy_message(), но from_chat_id и message_id берутся из апдейта.
        
        Use this method to copy messages of any kind. Service messages, paid media messages, giveaway messages, giveaway winners messages, and invoice messages can't be copied. A quiz poll can be copied only if the value of the field correct_option_ids is known to the bot. The method is analogous to the method forwardMessage, but the copied message doesn't have a link to the original message. Returns the MessageId of the sent message on success.
        
        https://core.telegram.org/bots/api#copymessage
        
        Args:
            chat_id: Unique identifier for the target chat or username of the target bot, supergroup or channel in the format @username
            message_thread_id: Unique identifier for the target message thread (topic) of a forum; for forum supergroups and private chats of bots with forum topic mode enabled only
            direct_messages_topic_id: Identifier of the direct messages topic to which the message will be sent; required if the message is sent to a direct messages chat
            message_id: Message identifier in the chat specified in from_chat_id
            video_start_timestamp: New start timestamp for the copied video in the message
            caption: New caption for media, 0-1024 characters after entities parsing. If not specified, the original caption is kept.
            parse_mode: Mode for parsing entities in the new caption. See formatting options for more details.
            caption_entities: A JSON-serialized list of special entities that appear in the new caption, which can be specified instead of parse_mode
            show_caption_above_media: Pass True if the caption must be shown above the message media. Ignored if a new caption isn't specified.
            disable_notification: Sends the message silently. Users will receive a notification with no sound.
            protect_content: Protects the contents of the sent message from forwarding and saving
            allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance.
            message_effect_id: Unique identifier of the message effect to be added to the message; only available when copying to private chats
            suggested_post_parameters: A JSON-serialized object containing the parameters of the suggested post to send; for direct messages chats only. If the message is sent as a reply to another suggested post, then that suggested post is automatically declined.
            reply_parameters: Description of the message to reply to
            reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user.
        """
        return await self.bot.copy_message(
            chat_id=chat_id,
            message_thread_id=message_thread_id,
            direct_messages_topic_id=direct_messages_topic_id,
            from_chat_id=self.chat_id,
            message_id=message_id if message_id is not None else self._require_message_id(),
            video_start_timestamp=video_start_timestamp,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            show_caption_above_media=show_caption_above_media,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def copy_messages(
        self,
        chat_id: Union[int, str],
        message_ids: List[int],
        *,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        remove_caption: Optional[bool] = None,
    ) -> List[MessageId]:
        """Как bot.copy_messages(), но from_chat_id и message_id берутся из апдейта.
        
        Use this method to copy messages of any kind. If some of the specified messages can't be found or copied, they are skipped. Service messages, paid media messages, giveaway messages, giveaway winners messages, and invoice messages can't be copied. A quiz poll can be copied only if the value of the field correct_option_ids is known to the bot. The method is analogous to the method forwardMessages, but the copied messages don't have a link to the original message. Album grouping is kept for copied messages. On success, an Array of MessageId of the sent messages is returned.
        
        https://core.telegram.org/bots/api#copymessages
        
        Args:
            chat_id: Unique identifier for the target chat or username of the target bot, supergroup or channel in the format @username
            message_thread_id: Unique identifier for the target message thread (topic) of a forum; for forum supergroups and private chats of bots with forum topic mode enabled only
            direct_messages_topic_id: Identifier of the direct messages topic to which the messages will be sent; required if the messages are sent to a direct messages chat
            message_ids: A JSON-serialized list of 1-100 identifiers of messages in the chat from_chat_id to copy. The identifiers must be specified in a strictly increasing order.
            disable_notification: Sends the messages silently. Users will receive a notification with no sound.
            protect_content: Protects the contents of the sent messages from forwarding and saving
            remove_caption: Pass True to copy the messages without their captions
        """
        return await self.bot.copy_messages(
            chat_id=chat_id,
            message_thread_id=message_thread_id,
            direct_messages_topic_id=direct_messages_topic_id,
            from_chat_id=self.chat_id,
            message_ids=message_ids,
            disable_notification=disable_notification,
            protect_content=protect_content,
            remove_caption=remove_caption,
        )

    async def answer_photo(
        self,
        photo: Union[InputFile, str],
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        show_caption_above_media: Optional[bool] = None,
        has_spoiler: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_photo(), но чат берётся из апдейта.
        
        Use this method to send photos. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendphoto
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
            message_thread_id: Unique identifier for the target message thread (topic) of a forum; for forum supergroups and private chats of bots with forum topic mode enabled only
            direct_messages_topic_id: Identifier of the direct messages topic to which the message will be sent; required if the message is sent to a direct messages chat
            ephemeral_message_parameters: A JSON-serialized object containing the parameters of the ephemeral message to send
            photo: Photo to send. Pass a file_id as String to send a photo that exists on the Telegram servers (recommended), pass an HTTP URL as a String for Telegram to get a photo from the Internet, or upload a new photo using multipart/form-data. The photo must be at most 10 MB in size. The photo's width and height must not exceed 10000 in total. Width and height ratio must be at most 20. More information on Sending Files: https://core.telegram.org/bots/api#sending-files
            caption: Photo caption (may also be used when resending photos by file_id), 0-1024 characters after entities parsing
            parse_mode: Mode for parsing entities in the photo caption. See formatting options for more details.
            caption_entities: A JSON-serialized list of special entities that appear in the caption, which can be specified instead of parse_mode
            show_caption_above_media: Pass True if the caption must be shown above the message media
            has_spoiler: Pass True if the photo needs to be covered with a spoiler animation
            disable_notification: Sends the message silently. Users will receive a notification with no sound.
            protect_content: Protects the contents of the sent message from forwarding and saving
            allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance.
            message_effect_id: Unique identifier of the message effect to be added to the message; for private chats only
            suggested_post_parameters: A JSON-serialized object containing the parameters of the suggested post to send; for direct messages chats only. If the message is sent as a reply to another suggested post, then that suggested post is automatically declined.
            reply_parameters: Description of the message to reply to
            reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user.
        """
        return await self.bot.send_photo(
            business_connection_id=self._or_default("business_connection_id", business_connection_id),
            chat_id=self.chat_id,
            message_thread_id=self._or_default("message_thread_id", message_thread_id),
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            photo=photo,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            show_caption_above_media=show_caption_above_media,
            has_spoiler=has_spoiler,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def reply_photo(
        self,
        photo: Union[InputFile, str],
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        show_caption_above_media: Optional[bool] = None,
        has_spoiler: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_photo(), но чат берётся из апдейта, сообщение цитирует сообщение апдейта.
        
        Use this method to send photos. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendphoto
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
            message_thread_id: Unique identifier for the target message thread (topic) of a forum; for forum supergroups and private chats of bots with forum topic mode enabled only
            direct_messages_topic_id: Identifier of the direct messages topic to which the message will be sent; required if the message is sent to a direct messages chat
            ephemeral_message_parameters: A JSON-serialized object containing the parameters of the ephemeral message to send
            photo: Photo to send. Pass a file_id as String to send a photo that exists on the Telegram servers (recommended), pass an HTTP URL as a String for Telegram to get a photo from the Internet, or upload a new photo using multipart/form-data. The photo must be at most 10 MB in size. The photo's width and height must not exceed 10000 in total. Width and height ratio must be at most 20. More information on Sending Files: https://core.telegram.org/bots/api#sending-files
            caption: Photo caption (may also be used when resending photos by file_id), 0-1024 characters after entities parsing
            parse_mode: Mode for parsing entities in the photo caption. See formatting options for more details.
            caption_entities: A JSON-serialized list of special entities that appear in the caption, which can be specified instead of parse_mode
            show_caption_above_media: Pass True if the caption must be shown above the message media
            has_spoiler: Pass True if the photo needs to be covered with a spoiler animation
            disable_notification: Sends the message silently. Users will receive a notification with no sound.
            protect_content: Protects the contents of the sent message from forwarding and saving
            allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance.
            message_effect_id: Unique identifier of the message effect to be added to the message; for private chats only
            suggested_post_parameters: A JSON-serialized object containing the parameters of the suggested post to send; for direct messages chats only. If the message is sent as a reply to another suggested post, then that suggested post is automatically declined.
            reply_parameters: Description of the message to reply to
            reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user.
        """
        return await self.bot.send_photo(
            business_connection_id=self._or_default("business_connection_id", business_connection_id),
            chat_id=self.chat_id,
            message_thread_id=self._or_default("message_thread_id", message_thread_id),
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            photo=photo,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            show_caption_above_media=show_caption_above_media,
            has_spoiler=has_spoiler,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters if reply_parameters is not None else self._reply_parameters(),
            reply_markup=reply_markup,
        )

    async def answer_live_photo(
        self,
        live_photo: Union[InputFile, str],
        photo: Union[InputFile, str],
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        show_caption_above_media: Optional[bool] = None,
        has_spoiler: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_live_photo(), но чат берётся из апдейта.
        
        Use this method to send live photos. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendlivephoto
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
            message_thread_id: Unique identifier for the target message thread (topic) of a forum; for forum supergroups and private chats of bots with forum topic mode enabled only
            direct_messages_topic_id: Identifier of the direct messages topic to which the message will be sent; required if the message is sent to a direct messages chat
            ephemeral_message_parameters: A JSON-serialized object containing the parameters of the ephemeral message to send
            live_photo: Live photo video to send. The video must be no longer than 10 seconds and must not exceed 10 MB in size. Pass a file_id as String to send a video that exists on the Telegram servers (recommended) or upload a new video using multipart/form-data. More information on Sending Files: https://core.telegram.org/bots/api#sending-files. Sending live photos by a URL is currently unsupported.
            photo: The static photo to send. Pass a file_id as String to send a photo that exists on the Telegram servers (recommended) or upload a new video using multipart/form-data. More information on Sending Files: https://core.telegram.org/bots/api#sending-files. Sending live photos by a URL is currently unsupported.
            caption: Video caption (may also be used when resending videos by file_id), 0-1024 characters after entities parsing
            parse_mode: Mode for parsing entities in the video caption. See formatting options for more details.
            caption_entities: A JSON-serialized list of special entities that appear in the caption, which can be specified instead of parse_mode
            show_caption_above_media: Pass True if the caption must be shown above the message media
            has_spoiler: Pass True if the video needs to be covered with a spoiler animation
            disable_notification: Sends the message silently. Users will receive a notification with no sound.
            protect_content: Protects the contents of the sent message from forwarding and saving
            allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance.
            message_effect_id: Unique identifier of the message effect to be added to the message; for private chats only
            suggested_post_parameters: A JSON-serialized object containing the parameters of the suggested post to send; for direct messages chats only. If the message is sent as a reply to another suggested post, then that suggested post is automatically declined.
            reply_parameters: Description of the message to reply to
            reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user.
        """
        return await self.bot.send_live_photo(
            business_connection_id=self._or_default("business_connection_id", business_connection_id),
            chat_id=self.chat_id,
            message_thread_id=self._or_default("message_thread_id", message_thread_id),
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            live_photo=live_photo,
            photo=photo,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            show_caption_above_media=show_caption_above_media,
            has_spoiler=has_spoiler,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def reply_live_photo(
        self,
        live_photo: Union[InputFile, str],
        photo: Union[InputFile, str],
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        show_caption_above_media: Optional[bool] = None,
        has_spoiler: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_live_photo(), но чат берётся из апдейта, сообщение цитирует сообщение апдейта.
        
        Use this method to send live photos. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendlivephoto
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
            message_thread_id: Unique identifier for the target message thread (topic) of a forum; for forum supergroups and private chats of bots with forum topic mode enabled only
            direct_messages_topic_id: Identifier of the direct messages topic to which the message will be sent; required if the message is sent to a direct messages chat
            ephemeral_message_parameters: A JSON-serialized object containing the parameters of the ephemeral message to send
            live_photo: Live photo video to send. The video must be no longer than 10 seconds and must not exceed 10 MB in size. Pass a file_id as String to send a video that exists on the Telegram servers (recommended) or upload a new video using multipart/form-data. More information on Sending Files: https://core.telegram.org/bots/api#sending-files. Sending live photos by a URL is currently unsupported.
            photo: The static photo to send. Pass a file_id as String to send a photo that exists on the Telegram servers (recommended) or upload a new video using multipart/form-data. More information on Sending Files: https://core.telegram.org/bots/api#sending-files. Sending live photos by a URL is currently unsupported.
            caption: Video caption (may also be used when resending videos by file_id), 0-1024 characters after entities parsing
            parse_mode: Mode for parsing entities in the video caption. See formatting options for more details.
            caption_entities: A JSON-serialized list of special entities that appear in the caption, which can be specified instead of parse_mode
            show_caption_above_media: Pass True if the caption must be shown above the message media
            has_spoiler: Pass True if the video needs to be covered with a spoiler animation
            disable_notification: Sends the message silently. Users will receive a notification with no sound.
            protect_content: Protects the contents of the sent message from forwarding and saving
            allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance.
            message_effect_id: Unique identifier of the message effect to be added to the message; for private chats only
            suggested_post_parameters: A JSON-serialized object containing the parameters of the suggested post to send; for direct messages chats only. If the message is sent as a reply to another suggested post, then that suggested post is automatically declined.
            reply_parameters: Description of the message to reply to
            reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user.
        """
        return await self.bot.send_live_photo(
            business_connection_id=self._or_default("business_connection_id", business_connection_id),
            chat_id=self.chat_id,
            message_thread_id=self._or_default("message_thread_id", message_thread_id),
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            live_photo=live_photo,
            photo=photo,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            show_caption_above_media=show_caption_above_media,
            has_spoiler=has_spoiler,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters if reply_parameters is not None else self._reply_parameters(),
            reply_markup=reply_markup,
        )

    async def answer_audio(
        self,
        audio: Union[InputFile, str],
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        duration: Optional[int] = None,
        performer: Optional[str] = None,
        title: Optional[str] = None,
        thumbnail: Optional[Union[InputFile, str]] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_audio(), но чат берётся из апдейта.
        
        Use this method to send audio files, if you want Telegram clients to display them in the music player. Your audio must be in the .MP3 or .M4A format. On success, the sent Message is returned. Bots can currently send audio files of up to 50 MB in size, this limit may be changed in the future.
        
        For sending voice messages, use the sendVoice method instead.
        
        https://core.telegram.org/bots/api#sendaudio
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
            message_thread_id: Unique identifier for the target message thread (topic) of a forum; for forum supergroups and private chats of bots with forum topic mode enabled only
            direct_messages_topic_id: Identifier of the direct messages topic to which the message will be sent; required if the message is sent to a direct messages chat
            ephemeral_message_parameters: A JSON-serialized object containing the parameters of the ephemeral message to send
            audio: Audio file to send. Pass a file_id as String to send an audio file that exists on the Telegram servers (recommended), pass an HTTP URL as a String for Telegram to get an audio file from the Internet, or upload a new one using multipart/form-data. More information on Sending Files: https://core.telegram.org/bots/api#sending-files
            caption: Audio caption, 0-1024 characters after entities parsing
            parse_mode: Mode for parsing entities in the audio caption. See formatting options for more details.
            caption_entities: A JSON-serialized list of special entities that appear in the caption, which can be specified instead of parse_mode
            duration: Duration of the audio in seconds
            performer: Performer
            title: Track name
            thumbnail: Thumbnail of the file sent; can be ignored if thumbnail generation for the file is supported server-side. The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail's width and height should not exceed 320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails can't be reused and can be only uploaded as a new file, so you can pass "attach://<file_attach_name>" if the thumbnail was uploaded using multipart/form-data under <file_attach_name>. More information on Sending Files: https://core.telegram.org/bots/api#sending-files
            disable_notification: Sends the message silently. Users will receive a notification with no sound.
            protect_content: Protects the contents of the sent message from forwarding and saving
            allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance.
            message_effect_id: Unique identifier of the message effect to be added to the message; for private chats only
            suggested_post_parameters: A JSON-serialized object containing the parameters of the suggested post to send; for direct messages chats only. If the message is sent as a reply to another suggested post, then that suggested post is automatically declined.
            reply_parameters: Description of the message to reply to
            reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user.
        """
        return await self.bot.send_audio(
            business_connection_id=self._or_default("business_connection_id", business_connection_id),
            chat_id=self.chat_id,
            message_thread_id=self._or_default("message_thread_id", message_thread_id),
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            audio=audio,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            duration=duration,
            performer=performer,
            title=title,
            thumbnail=thumbnail,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def reply_audio(
        self,
        audio: Union[InputFile, str],
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        duration: Optional[int] = None,
        performer: Optional[str] = None,
        title: Optional[str] = None,
        thumbnail: Optional[Union[InputFile, str]] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_audio(), но чат берётся из апдейта, сообщение цитирует сообщение апдейта.
        
        Use this method to send audio files, if you want Telegram clients to display them in the music player. Your audio must be in the .MP3 or .M4A format. On success, the sent Message is returned. Bots can currently send audio files of up to 50 MB in size, this limit may be changed in the future.
        
        For sending voice messages, use the sendVoice method instead.
        
        https://core.telegram.org/bots/api#sendaudio
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
            message_thread_id: Unique identifier for the target message thread (topic) of a forum; for forum supergroups and private chats of bots with forum topic mode enabled only
            direct_messages_topic_id: Identifier of the direct messages topic to which the message will be sent; required if the message is sent to a direct messages chat
            ephemeral_message_parameters: A JSON-serialized object containing the parameters of the ephemeral message to send
            audio: Audio file to send. Pass a file_id as String to send an audio file that exists on the Telegram servers (recommended), pass an HTTP URL as a String for Telegram to get an audio file from the Internet, or upload a new one using multipart/form-data. More information on Sending Files: https://core.telegram.org/bots/api#sending-files
            caption: Audio caption, 0-1024 characters after entities parsing
            parse_mode: Mode for parsing entities in the audio caption. See formatting options for more details.
            caption_entities: A JSON-serialized list of special entities that appear in the caption, which can be specified instead of parse_mode
            duration: Duration of the audio in seconds
            performer: Performer
            title: Track name
            thumbnail: Thumbnail of the file sent; can be ignored if thumbnail generation for the file is supported server-side. The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail's width and height should not exceed 320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails can't be reused and can be only uploaded as a new file, so you can pass "attach://<file_attach_name>" if the thumbnail was uploaded using multipart/form-data under <file_attach_name>. More information on Sending Files: https://core.telegram.org/bots/api#sending-files
            disable_notification: Sends the message silently. Users will receive a notification with no sound.
            protect_content: Protects the contents of the sent message from forwarding and saving
            allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance.
            message_effect_id: Unique identifier of the message effect to be added to the message; for private chats only
            suggested_post_parameters: A JSON-serialized object containing the parameters of the suggested post to send; for direct messages chats only. If the message is sent as a reply to another suggested post, then that suggested post is automatically declined.
            reply_parameters: Description of the message to reply to
            reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user.
        """
        return await self.bot.send_audio(
            business_connection_id=self._or_default("business_connection_id", business_connection_id),
            chat_id=self.chat_id,
            message_thread_id=self._or_default("message_thread_id", message_thread_id),
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            audio=audio,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            duration=duration,
            performer=performer,
            title=title,
            thumbnail=thumbnail,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters if reply_parameters is not None else self._reply_parameters(),
            reply_markup=reply_markup,
        )

    async def answer_document(
        self,
        document: Union[InputFile, str],
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        thumbnail: Optional[Union[InputFile, str]] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        disable_content_type_detection: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_document(), но чат берётся из апдейта.
        
        Use this method to send general files. On success, the sent Message is returned. Bots can currently send files of any type of up to 50 MB in size, this limit may be changed in the future.
        
        https://core.telegram.org/bots/api#senddocument
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
            message_thread_id: Unique identifier for the target message thread (topic) of a forum; for forum supergroups and private chats of bots with forum topic mode enabled only
            direct_messages_topic_id: Identifier of the direct messages topic to which the message will be sent; required if the message is sent to a direct messages chat
            ephemeral_message_parameters: A JSON-serialized object containing the parameters of the ephemeral message to send
            document: File to send. Pass a file_id as String to send a file that exists on the Telegram servers (recommended), pass an HTTP URL as a String for Telegram to get a file from the Internet, or upload a new one using multipart/form-data. More information on Sending Files: https://core.telegram.org/bots/api#sending-files
            thumbnail: Thumbnail of the file sent; can be ignored if thumbnail generation for the file is supported server-side. The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail's width and height should not exceed 320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails can't be reused and can be only uploaded as a new file, so you can pass "attach://<file_attach_name>" if the thumbnail was uploaded using multipart/form-data under <file_attach_name>. More information on Sending Files: https://core.telegram.org/bots/api#sending-files
            caption: Document caption (may also be used when resending documents by file_id), 0-1024 characters after entities parsing
            parse_mode: Mode for parsing entities in the document caption. See formatting options for more details.
            caption_entities: A JSON-serialized list of special entities that appear in the caption, which can be specified instead of parse_mode
            disable_content_type_detection: Disables automatic server-side content type detection for files uploaded using multipart/form-data
            disable_notification: Sends the message silently. Users will receive a notification with no sound.
            protect_content: Protects the contents of the sent message from forwarding and saving
            allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance.
            message_effect_id: Unique identifier of the message effect to be added to the message; for private chats only
            suggested_post_parameters: A JSON-serialized object containing the parameters of the suggested post to send; for direct messages chats only. If the message is sent as a reply to another suggested post, then that suggested post is automatically declined.
            reply_parameters: Description of the message to reply to
            reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user.
        """
        return await self.bot.send_document(
            business_connection_id=self._or_default("business_connection_id", business_connection_id),
            chat_id=self.chat_id,
            message_thread_id=self._or_default("message_thread_id", message_thread_id),
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            document=document,
            thumbnail=thumbnail,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            disable_content_type_detection=disable_content_type_detection,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def reply_document(
        self,
        document: Union[InputFile, str],
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        thumbnail: Optional[Union[InputFile, str]] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        disable_content_type_detection: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_document(), но чат берётся из апдейта, сообщение цитирует сообщение апдейта.
        
        Use this method to send general files. On success, the sent Message is returned. Bots can currently send files of any type of up to 50 MB in size, this limit may be changed in the future.
        
        https://core.telegram.org/bots/api#senddocument
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
            message_thread_id: Unique identifier for the target message thread (topic) of a forum; for forum supergroups and private chats of bots with forum topic mode enabled only
            direct_messages_topic_id: Identifier of the direct messages topic to which the message will be sent; required if the message is sent to a direct messages chat
            ephemeral_message_parameters: A JSON-serialized object containing the parameters of the ephemeral message to send
            document: File to send. Pass a file_id as String to send a file that exists on the Telegram servers (recommended), pass an HTTP URL as a String for Telegram to get a file from the Internet, or upload a new one using multipart/form-data. More information on Sending Files: https://core.telegram.org/bots/api#sending-files
            thumbnail: Thumbnail of the file sent; can be ignored if thumbnail generation for the file is supported server-side. The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail's width and height should not exceed 320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails can't be reused and can be only uploaded as a new file, so you can pass "attach://<file_attach_name>" if the thumbnail was uploaded using multipart/form-data under <file_attach_name>. More information on Sending Files: https://core.telegram.org/bots/api#sending-files
            caption: Document caption (may also be used when resending documents by file_id), 0-1024 characters after entities parsing
            parse_mode: Mode for parsing entities in the document caption. See formatting options for more details.
            caption_entities: A JSON-serialized list of special entities that appear in the caption, which can be specified instead of parse_mode
            disable_content_type_detection: Disables automatic server-side content type detection for files uploaded using multipart/form-data
            disable_notification: Sends the message silently. Users will receive a notification with no sound.
            protect_content: Protects the contents of the sent message from forwarding and saving
            allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance.
            message_effect_id: Unique identifier of the message effect to be added to the message; for private chats only
            suggested_post_parameters: A JSON-serialized object containing the parameters of the suggested post to send; for direct messages chats only. If the message is sent as a reply to another suggested post, then that suggested post is automatically declined.
            reply_parameters: Description of the message to reply to
            reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user.
        """
        return await self.bot.send_document(
            business_connection_id=self._or_default("business_connection_id", business_connection_id),
            chat_id=self.chat_id,
            message_thread_id=self._or_default("message_thread_id", message_thread_id),
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            document=document,
            thumbnail=thumbnail,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            disable_content_type_detection=disable_content_type_detection,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters if reply_parameters is not None else self._reply_parameters(),
            reply_markup=reply_markup,
        )

    async def answer_video(
        self,
        video: Union[InputFile, str],
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        duration: Optional[int] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        thumbnail: Optional[Union[InputFile, str]] = None,
        cover: Optional[Union[InputFile, str]] = None,
        start_timestamp: Optional[int] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        show_caption_above_media: Optional[bool] = None,
        has_spoiler: Optional[bool] = None,
        supports_streaming: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_video(), но чат берётся из апдейта.
        
        Use this method to send video files, Telegram clients support MPEG4 videos (other formats may be sent as Document). On success, the sent Message is returned. Bots can currently send video files of up to 50 MB in size, this limit may be changed in the future.
        
        https://core.telegram.org/bots/api#sendvideo
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
            message_thread_id: Unique identifier for the target message thread (topic) of a forum; for forum supergroups and private chats of bots with forum topic mode enabled only
            direct_messages_topic_id: Identifier of the direct messages topic to which the message will be sent; required if the message is sent to a direct messages chat
            ephemeral_message_parameters: A JSON-serialized object containing the parameters of the ephemeral message to send
            video: Video to send. Pass a file_id as String to send a video that exists on the Telegram servers (recommended), pass an HTTP URL as a String for Telegram to get a video from the Internet, or upload a new video using multipart/form-data. More information on Sending Files: https://core.telegram.org/bots/api#sending-files
            duration: Duration of sent video in seconds
            width: Video width
            height: Video height
            thumbnail: Thumbnail of the file sent; can be ignored if thumbnail generation for the file is supported server-side. The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail's width and height should not exceed 320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails can't be reused and can be only uploaded as a new file, so you can pass "attach://<file_attach_name>" if the thumbnail was uploaded using multipart/form-data under <file_attach_name>. More information on Sending Files: https://core.telegram.org/bots/api#sending-files
            cover: Cover for the video in the message. Pass a file_id to send a file that exists on the Telegram servers (recommended), pass an HTTP URL for Telegram to get a file from the Internet, or pass "attach://<file_attach_name>" to upload a new one using multipart/form-data under <file_attach_name> name. More information on Sending Files: https://core.telegram.org/bots/api#sending-files
            start_timestamp: Start timestamp for the video in the message
            caption: Video caption (may also be used when resending videos by file_id), 0-1024 characters after entities parsing
            parse_mode: Mode for parsing entities in the video caption. See formatting options for more details.
            caption_entities: A JSON-serialized list of special entities that appear in the caption, which can be specified instead of parse_mode
            show_caption_above_media: Pass True if the caption must be shown above the message media
            has_spoiler: Pass True if the video needs to be covered with a spoiler animation
            supports_streaming: Pass True if the uploaded video is suitable for streaming
            disable_notification: Sends the message silently. Users will receive a notification with no sound.
            protect_content: Protects the contents of the sent message from forwarding and saving
            allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance.
            message_effect_id: Unique identifier of the message effect to be added to the message; for private chats only
            suggested_post_parameters: A JSON-serialized object containing the parameters of the suggested post to send; for direct messages chats only. If the message is sent as a reply to another suggested post, then that suggested post is automatically declined.
            reply_parameters: Description of the message to reply to
            reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user.
        """
        return await self.bot.send_video(
            business_connection_id=self._or_default("business_connection_id", business_connection_id),
            chat_id=self.chat_id,
            message_thread_id=self._or_default("message_thread_id", message_thread_id),
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            video=video,
            duration=duration,
            width=width,
            height=height,
            thumbnail=thumbnail,
            cover=cover,
            start_timestamp=start_timestamp,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            show_caption_above_media=show_caption_above_media,
            has_spoiler=has_spoiler,
            supports_streaming=supports_streaming,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def reply_video(
        self,
        video: Union[InputFile, str],
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        duration: Optional[int] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        thumbnail: Optional[Union[InputFile, str]] = None,
        cover: Optional[Union[InputFile, str]] = None,
        start_timestamp: Optional[int] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        show_caption_above_media: Optional[bool] = None,
        has_spoiler: Optional[bool] = None,
        supports_streaming: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_video(), но чат берётся из апдейта, сообщение цитирует сообщение апдейта.
        
        Use this method to send video files, Telegram clients support MPEG4 videos (other formats may be sent as Document). On success, the sent Message is returned. Bots can currently send video files of up to 50 MB in size, this limit may be changed in the future.
        
        https://core.telegram.org/bots/api#sendvideo
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
            message_thread_id: Unique identifier for the target message thread (topic) of a forum; for forum supergroups and private chats of bots with forum topic mode enabled only
            direct_messages_topic_id: Identifier of the direct messages topic to which the message will be sent; required if the message is sent to a direct messages chat
            ephemeral_message_parameters: A JSON-serialized object containing the parameters of the ephemeral message to send
            video: Video to send. Pass a file_id as String to send a video that exists on the Telegram servers (recommended), pass an HTTP URL as a String for Telegram to get a video from the Internet, or upload a new video using multipart/form-data. More information on Sending Files: https://core.telegram.org/bots/api#sending-files
            duration: Duration of sent video in seconds
            width: Video width
            height: Video height
            thumbnail: Thumbnail of the file sent; can be ignored if thumbnail generation for the file is supported server-side. The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail's width and height should not exceed 320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails can't be reused and can be only uploaded as a new file, so you can pass "attach://<file_attach_name>" if the thumbnail was uploaded using multipart/form-data under <file_attach_name>. More information on Sending Files: https://core.telegram.org/bots/api#sending-files
            cover: Cover for the video in the message. Pass a file_id to send a file that exists on the Telegram servers (recommended), pass an HTTP URL for Telegram to get a file from the Internet, or pass "attach://<file_attach_name>" to upload a new one using multipart/form-data under <file_attach_name> name. More information on Sending Files: https://core.telegram.org/bots/api#sending-files
            start_timestamp: Start timestamp for the video in the message
            caption: Video caption (may also be used when resending videos by file_id), 0-1024 characters after entities parsing
            parse_mode: Mode for parsing entities in the video caption. See formatting options for more details.
            caption_entities: A JSON-serialized list of special entities that appear in the caption, which can be specified instead of parse_mode
            show_caption_above_media: Pass True if the caption must be shown above the message media
            has_spoiler: Pass True if the video needs to be covered with a spoiler animation
            supports_streaming: Pass True if the uploaded video is suitable for streaming
            disable_notification: Sends the message silently. Users will receive a notification with no sound.
            protect_content: Protects the contents of the sent message from forwarding and saving
            allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance.
            message_effect_id: Unique identifier of the message effect to be added to the message; for private chats only
            suggested_post_parameters: A JSON-serialized object containing the parameters of the suggested post to send; for direct messages chats only. If the message is sent as a reply to another suggested post, then that suggested post is automatically declined.
            reply_parameters: Description of the message to reply to
            reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user.
        """
        return await self.bot.send_video(
            business_connection_id=self._or_default("business_connection_id", business_connection_id),
            chat_id=self.chat_id,
            message_thread_id=self._or_default("message_thread_id", message_thread_id),
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            video=video,
            duration=duration,
            width=width,
            height=height,
            thumbnail=thumbnail,
            cover=cover,
            start_timestamp=start_timestamp,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            show_caption_above_media=show_caption_above_media,
            has_spoiler=has_spoiler,
            supports_streaming=supports_streaming,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters if reply_parameters is not None else self._reply_parameters(),
            reply_markup=reply_markup,
        )

    async def answer_animation(
        self,
        animation: Union[InputFile, str],
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        duration: Optional[int] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        thumbnail: Optional[Union[InputFile, str]] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        show_caption_above_media: Optional[bool] = None,
        has_spoiler: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_animation(), но чат берётся из апдейта.
        
        Use this method to send animation files (GIF or H.264/MPEG-4 AVC video without sound). On success, the sent Message is returned. Bots can currently send animation files of up to 50 MB in size, this limit may be changed in the future.
        
        https://core.telegram.org/bots/api#sendanimation
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
            message_thread_id: Unique identifier for the target message thread (topic) of a forum; for forum supergroups and private chats of bots with forum topic mode enabled only
            direct_messages_topic_id: Identifier of the direct messages topic to which the message will be sent; required if the message is sent to a direct messages chat
            ephemeral_message_parameters: A JSON-serialized object containing the parameters of the ephemeral message to send
            animation: Animation to send. Pass a file_id as String to send an animation that exists on the Telegram servers (recommended), pass an HTTP URL as a String for Telegram to get an animation from the Internet, or upload a new animation using multipart/form-data. More information on Sending Files: https://core.telegram.org/bots/api#sending-files
            duration: Duration of sent animation in seconds
            width: Animation width
            height: Animation height
            thumbnail: Thumbnail of the file sent; can be ignored if thumbnail generation for the file is supported server-side. The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail's width and height should not exceed 320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails can't be reused and can be only uploaded as a new file, so you can pass "attach://<file_attach_name>" if the thumbnail was uploaded using multipart/form-data under <file_attach_name>. More information on Sending Files: https://core.telegram.org/bots/api#sending-files
            caption: Animation caption (may also be used when resending animation by file_id), 0-1024 characters after entities parsing
            parse_mode: Mode for parsing entities in the animation caption. See formatting options for more details.
            caption_entities: A JSON-serialized list of special entities that appear in the caption, which can be specified instead of parse_mode
            show_caption_above_media: Pass True if the caption must be shown above the message media
            has_spoiler: Pass True if the animation needs to be covered with a spoiler animation
            disable_notification: Sends the message silently. Users will receive a notification with no sound.
            protect_content: Protects the contents of the sent message from forwarding and saving
            allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance.
            message_effect_id: Unique identifier of the message effect to be added to the message; for private chats only
            suggested_post_parameters: A JSON-serialized object containing the parameters of the suggested post to send; for direct messages chats only. If the message is sent as a reply to another suggested post, then that suggested post is automatically declined.
            reply_parameters: Description of the message to reply to
            reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user.
        """
        return await self.bot.send_animation(
            business_connection_id=self._or_default("business_connection_id", business_connection_id),
            chat_id=self.chat_id,
            message_thread_id=self._or_default("message_thread_id", message_thread_id),
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            animation=animation,
            duration=duration,
            width=width,
            height=height,
            thumbnail=thumbnail,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            show_caption_above_media=show_caption_above_media,
            has_spoiler=has_spoiler,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def reply_animation(
        self,
        animation: Union[InputFile, str],
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        duration: Optional[int] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        thumbnail: Optional[Union[InputFile, str]] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        show_caption_above_media: Optional[bool] = None,
        has_spoiler: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_animation(), но чат берётся из апдейта, сообщение цитирует сообщение апдейта.
        
        Use this method to send animation files (GIF or H.264/MPEG-4 AVC video without sound). On success, the sent Message is returned. Bots can currently send animation files of up to 50 MB in size, this limit may be changed in the future.
        
        https://core.telegram.org/bots/api#sendanimation
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
            message_thread_id: Unique identifier for the target message thread (topic) of a forum; for forum supergroups and private chats of bots with forum topic mode enabled only
            direct_messages_topic_id: Identifier of the direct messages topic to which the message will be sent; required if the message is sent to a direct messages chat
            ephemeral_message_parameters: A JSON-serialized object containing the parameters of the ephemeral message to send
            animation: Animation to send. Pass a file_id as String to send an animation that exists on the Telegram servers (recommended), pass an HTTP URL as a String for Telegram to get an animation from the Internet, or upload a new animation using multipart/form-data. More information on Sending Files: https://core.telegram.org/bots/api#sending-files
            duration: Duration of sent animation in seconds
            width: Animation width
            height: Animation height
            thumbnail: Thumbnail of the file sent; can be ignored if thumbnail generation for the file is supported server-side. The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail's width and height should not exceed 320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails can't be reused and can be only uploaded as a new file, so you can pass "attach://<file_attach_name>" if the thumbnail was uploaded using multipart/form-data under <file_attach_name>. More information on Sending Files: https://core.telegram.org/bots/api#sending-files
            caption: Animation caption (may also be used when resending animation by file_id), 0-1024 characters after entities parsing
            parse_mode: Mode for parsing entities in the animation caption. See formatting options for more details.
            caption_entities: A JSON-serialized list of special entities that appear in the caption, which can be specified instead of parse_mode
            show_caption_above_media: Pass True if the caption must be shown above the message media
            has_spoiler: Pass True if the animation needs to be covered with a spoiler animation
            disable_notification: Sends the message silently. Users will receive a notification with no sound.
            protect_content: Protects the contents of the sent message from forwarding and saving
            allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance.
            message_effect_id: Unique identifier of the message effect to be added to the message; for private chats only
            suggested_post_parameters: A JSON-serialized object containing the parameters of the suggested post to send; for direct messages chats only. If the message is sent as a reply to another suggested post, then that suggested post is automatically declined.
            reply_parameters: Description of the message to reply to
            reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user.
        """
        return await self.bot.send_animation(
            business_connection_id=self._or_default("business_connection_id", business_connection_id),
            chat_id=self.chat_id,
            message_thread_id=self._or_default("message_thread_id", message_thread_id),
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            animation=animation,
            duration=duration,
            width=width,
            height=height,
            thumbnail=thumbnail,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            show_caption_above_media=show_caption_above_media,
            has_spoiler=has_spoiler,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters if reply_parameters is not None else self._reply_parameters(),
            reply_markup=reply_markup,
        )

    async def answer_voice(
        self,
        voice: Union[InputFile, str],
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        duration: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_voice(), но чат берётся из апдейта.
        
        Use this method to send audio files, if you want Telegram clients to display the file as a playable voice message. For this to work, your audio must be in an .OGG file encoded with OPUS, or in .MP3 format, or in .M4A format (other formats may be sent as Audio or Document). On success, the sent Message is returned. Bots can currently send voice messages of up to 50 MB in size, this limit may be changed in the future.
        
        https://core.telegram.org/bots/api#sendvoice
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
            message_thread_id: Unique identifier for the target message thread (topic) of a forum; for forum supergroups and private chats of bots with forum topic mode enabled only
            direct_messages_topic_id: Identifier of the direct messages topic to which the message will be sent; required if the message is sent to a direct messages chat
            ephemeral_message_parameters: A JSON-serialized object containing the parameters of the ephemeral message to send
            voice: Audio file to send. Pass a file_id as String to send a file that exists on the Telegram servers (recommended), pass an HTTP URL as a String for Telegram to get a file from the Internet, or upload a new one using multipart/form-data. More information on Sending Files: https://core.telegram.org/bots/api#sending-files
            caption: Voice message caption, 0-1024 characters after entities parsing
            parse_mode: Mode for parsing entities in the voice message caption. See formatting options for more details.
            caption_entities: A JSON-serialized list of special entities that appear in the caption, which can be specified instead of parse_mode
            duration: Duration of the voice message in seconds
            disable_notification: Sends the message silently. Users will receive a notification with no sound.
            protect_content: Protects the contents of the sent message from forwarding and saving
            allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance.
            message_effect_id: Unique identifier of the message effect to be added to the message; for private chats only
            suggested_post_parameters: A JSON-serialized object containing the parameters of the suggested post to send; for direct messages chats only. If the message is sent as a reply to another suggested post, then that suggested post is automatically declined.
            reply_parameters: Description of the message to reply to
            reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user.
        """
        return await self.bot.send_voice(
            business_connection_id=self._or_default("business_connection_id", business_connection_id),
            chat_id=self.chat_id,
            message_thread_id=self._or_default("message_thread_id", message_thread_id),
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            voice=voice,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            duration=duration,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def reply_voice(
        self,
        voice: Union[InputFile, str],
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        duration: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_voice(), но чат берётся из апдейта, сообщение цитирует сообщение апдейта.
        
        Use this method to send audio files, if you want Telegram clients to display the file as a playable voice message. For this to work, your audio must be in an .OGG file encoded with OPUS, or in .MP3 format, or in .M4A format (other formats may be sent as Audio or Document). On success, the sent Message is returned. Bots can currently send voice messages of up to 50 MB in size, this limit may be changed in the future.
        
        https://core.telegram.org/bots/api#sendvoice
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
            message_thread_id: Unique identifier for the target message thread (topic) of a forum; for forum supergroups and private chats of bots with forum topic mode enabled only
            direct_messages_topic_id: Identifier of the direct messages topic to which the message will be sent; required if the message is sent to a direct messages chat
            ephemeral_message_parameters: A JSON-serialized object containing the parameters of the ephemeral message to send
            voice: Audio file to send. Pass a file_id as String to send a file that exists on the Telegram servers (recommended), pass an HTTP URL as a String for Telegram to get a file from the Internet, or upload a new one using multipart/form-data. More information on Sending Files: https://core.telegram.org/bots/api#sending-files
            caption: Voice message caption, 0-1024 characters after entities parsing
            parse_mode: Mode for parsing entities in the voice message caption. See formatting options for more details.
            caption_entities: A JSON-serialized list of special entities that appear in the caption, which can be specified instead of parse_mode
            duration: Duration of the voice message in seconds
            disable_notification: Sends the message silently. Users will receive a notification with no sound.
            protect_content: Protects the contents of the sent message from forwarding and saving
            allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance.
            message_effect_id: Unique identifier of the message effect to be added to the message; for private chats only
            suggested_post_parameters: A JSON-serialized object containing the parameters of the suggested post to send; for direct messages chats only. If the message is sent as a reply to another suggested post, then that suggested post is automatically declined.
            reply_parameters: Description of the message to reply to
            reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user.
        """
        return await self.bot.send_voice(
            business_connection_id=self._or_default("business_connection_id", business_connection_id),
            chat_id=self.chat_id,
            message_thread_id=self._or_default("message_thread_id", message_thread_id),
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            voice=voice,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            duration=duration,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters if reply_parameters is not None else self._reply_parameters(),
            reply_markup=reply_markup,
        )

    async def answer_video_note(
        self,
        video_note: Union[InputFile, str],
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        duration: Optional[int] = None,
        length: Optional[int] = None,
        thumbnail: Optional[Union[InputFile, str]] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_video_note(), но чат берётся из апдейта.
        
        Use this method to send a rounded square MPEG4 video of up to 1 minute long. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendvideonote
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
            message_thread_id: Unique identifier for the target message thread (topic) of a forum; for forum supergroups and private chats of bots with forum topic mode enabled only
            direct_messages_topic_id: Identifier of the direct messages topic to which the message will be sent; required if the message is sent to a direct messages chat
            ephemeral_message_parameters: A JSON-serialized object containing the parameters of the ephemeral message to send
            video_note: Video note to send. Pass a file_id as String to send a video note that exists on the Telegram servers (recommended) or upload a new video using multipart/form-data. More information on Sending Files: https://core.telegram.org/bots/api#sending-files. Sending video notes by a URL is currently unsupported.
            duration: Duration of sent video in seconds
            length: Video width and height, i.e. diameter of the video message
            thumbnail: Thumbnail of the file sent; can be ignored if thumbnail generation for the file is supported server-side. The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail's width and height should not exceed 320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails can't be reused and can be only uploaded as a new file, so you can pass "attach://<file_attach_name>" if the thumbnail was uploaded using multipart/form-data under <file_attach_name>. More information on Sending Files: https://core.telegram.org/bots/api#sending-files
            disable_notification: Sends the message silently. Users will receive a notification with no sound.
            protect_content: Protects the contents of the sent message from forwarding and saving
            allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance.
            message_effect_id: Unique identifier of the message effect to be added to the message; for private chats only
            suggested_post_parameters: A JSON-serialized object containing the parameters of the suggested post to send; for direct messages chats only. If the message is sent as a reply to another suggested post, then that suggested post is automatically declined.
            reply_parameters: Description of the message to reply to
            reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user.
        """
        return await self.bot.send_video_note(
            business_connection_id=self._or_default("business_connection_id", business_connection_id),
            chat_id=self.chat_id,
            message_thread_id=self._or_default("message_thread_id", message_thread_id),
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            video_note=video_note,
            duration=duration,
            length=length,
            thumbnail=thumbnail,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def reply_video_note(
        self,
        video_note: Union[InputFile, str],
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        duration: Optional[int] = None,
        length: Optional[int] = None,
        thumbnail: Optional[Union[InputFile, str]] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_video_note(), но чат берётся из апдейта, сообщение цитирует сообщение апдейта.
        
        Use this method to send a rounded square MPEG4 video of up to 1 minute long. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendvideonote
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
            message_thread_id: Unique identifier for the target message thread (topic) of a forum; for forum supergroups and private chats of bots with forum topic mode enabled only
            direct_messages_topic_id: Identifier of the direct messages topic to which the message will be sent; required if the message is sent to a direct messages chat
            ephemeral_message_parameters: A JSON-serialized object containing the parameters of the ephemeral message to send
            video_note: Video note to send. Pass a file_id as String to send a video note that exists on the Telegram servers (recommended) or upload a new video using multipart/form-data. More information on Sending Files: https://core.telegram.org/bots/api#sending-files. Sending video notes by a URL is currently unsupported.
            duration: Duration of sent video in seconds
            length: Video width and height, i.e. diameter of the video message
            thumbnail: Thumbnail of the file sent; can be ignored if thumbnail generation for the file is supported server-side. The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail's width and height should not exceed 320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails can't be reused and can be only uploaded as a new file, so you can pass "attach://<file_attach_name>" if the thumbnail was uploaded using multipart/form-data under <file_attach_name>. More information on Sending Files: https://core.telegram.org/bots/api#sending-files
            disable_notification: Sends the message silently. Users will receive a notification with no sound.
            protect_content: Protects the contents of the sent message from forwarding and saving
            allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance.
            message_effect_id: Unique identifier of the message effect to be added to the message; for private chats only
            suggested_post_parameters: A JSON-serialized object containing the parameters of the suggested post to send; for direct messages chats only. If the message is sent as a reply to another suggested post, then that suggested post is automatically declined.
            reply_parameters: Description of the message to reply to
            reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user.
        """
        return await self.bot.send_video_note(
            business_connection_id=self._or_default("business_connection_id", business_connection_id),
            chat_id=self.chat_id,
            message_thread_id=self._or_default("message_thread_id", message_thread_id),
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            video_note=video_note,
            duration=duration,
            length=length,
            thumbnail=thumbnail,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters if reply_parameters is not None else self._reply_parameters(),
            reply_markup=reply_markup,
        )

    async def answer_paid_media(
        self,
        star_count: int,
        media: List[InputPaidMedia],
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        payload: Optional[str] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        show_caption_above_media: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_paid_media(), но чат берётся из апдейта.
        
        Use this method to send paid media. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendpaidmedia
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
            message_thread_id: Unique identifier for the target message thread (topic) of a forum; for forum supergroups and private chats of bots with forum topic mode enabled only
            direct_messages_topic_id: Identifier of the direct messages topic to which the message will be sent; required if the message is sent to a direct messages chat
            star_count: The number of Telegram Stars that must be paid to buy access to the media; 1-25000
            media: A JSON-serialized Array describing the media to be sent; up to 10 items
            payload: Bot-defined paid media payload, 0-128 bytes. This will not be displayed to the user, use it for your internal processes.
            caption: Media caption, 0-1024 characters after entities parsing
            parse_mode: Mode for parsing entities in the media caption. See formatting options for more details.
            caption_entities: A JSON-serialized list of special entities that appear in the caption, which can be specified instead of parse_mode
            show_caption_above_media: Pass True if the caption must be shown above the message media
            disable_notification: Sends the message silently. Users will receive a notification with no sound.
            protect_content: Protects the contents of the sent message from forwarding and saving
            allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance.
            suggested_post_parameters: A JSON-serialized object containing the parameters of the suggested post to send; for direct messages chats only. If the message is sent as a reply to another suggested post, then that suggested post is automatically declined.
            reply_parameters: Description of the message to reply to
            reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user.
        """
        return await self.bot.send_paid_media(
            business_connection_id=self._or_default("business_connection_id", business_connection_id),
            chat_id=self.chat_id,
            message_thread_id=self._or_default("message_thread_id", message_thread_id),
            direct_messages_topic_id=direct_messages_topic_id,
            star_count=star_count,
            media=media,
            payload=payload,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            show_caption_above_media=show_caption_above_media,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def reply_paid_media(
        self,
        star_count: int,
        media: List[InputPaidMedia],
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        payload: Optional[str] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        show_caption_above_media: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_paid_media(), но чат берётся из апдейта, сообщение цитирует сообщение апдейта.
        
        Use this method to send paid media. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendpaidmedia
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
            message_thread_id: Unique identifier for the target message thread (topic) of a forum; for forum supergroups and private chats of bots with forum topic mode enabled only
            direct_messages_topic_id: Identifier of the direct messages topic to which the message will be sent; required if the message is sent to a direct messages chat
            star_count: The number of Telegram Stars that must be paid to buy access to the media; 1-25000
            media: A JSON-serialized Array describing the media to be sent; up to 10 items
            payload: Bot-defined paid media payload, 0-128 bytes. This will not be displayed to the user, use it for your internal processes.
            caption: Media caption, 0-1024 characters after entities parsing
            parse_mode: Mode for parsing entities in the media caption. See formatting options for more details.
            caption_entities: A JSON-serialized list of special entities that appear in the caption, which can be specified instead of parse_mode
            show_caption_above_media: Pass True if the caption must be shown above the message media
            disable_notification: Sends the message silently. Users will receive a notification with no sound.
            protect_content: Protects the contents of the sent message from forwarding and saving
            allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance.
            suggested_post_parameters: A JSON-serialized object containing the parameters of the suggested post to send; for direct messages chats only. If the message is sent as a reply to another suggested post, then that suggested post is automatically declined.
            reply_parameters: Description of the message to reply to
            reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user.
        """
        return await self.bot.send_paid_media(
            business_connection_id=self._or_default("business_connection_id", business_connection_id),
            chat_id=self.chat_id,
            message_thread_id=self._or_default("message_thread_id", message_thread_id),
            direct_messages_topic_id=direct_messages_topic_id,
            star_count=star_count,
            media=media,
            payload=payload,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            show_caption_above_media=show_caption_above_media,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters if reply_parameters is not None else self._reply_parameters(),
            reply_markup=reply_markup,
        )

    async def answer_media_group(
        self,
        media: Union[List[InputMediaAudio], List[InputMediaDocument], List[InputMediaLivePhoto], List[InputMediaPhoto], List[InputMediaVideo]],
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        reply_parameters: Optional[ReplyParameters] = None,
    ) -> List[Message]:
        """Как bot.send_media_group(), но чат берётся из апдейта.
        
        Use this method to send a group of photos, live photos, videos, documents or audios as an album. Documents and audio files can be only grouped in an album with messages of the same type. On success, an Array of Message objects that were sent is returned.
        
        https://core.telegram.org/bots/api#sendmediagroup
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
            message_thread_id: Unique identifier for the target message thread (topic) of a forum; for forum supergroups and private chats of bots with forum topic mode enabled only
            direct_messages_topic_id: Identifier of the direct messages topic to which the messages will be sent; required if the messages are sent to a direct messages chat
            media: A JSON-serialized Array describing messages to be sent, must include 2-10 items
            disable_notification: Sends messages silently. Users will receive a notification with no sound.
            protect_content: Protects the contents of the sent messages from forwarding and saving
            allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance.
            message_effect_id: Unique identifier of the message effect to be added to the message; for private chats only
            reply_parameters: Description of the message to reply to
        """
        return await self.bot.send_media_group(
            business_connection_id=self._or_default("business_connection_id", business_connection_id),
            chat_id=self.chat_id,
            message_thread_id=self._or_default("message_thread_id", message_thread_id),
            direct_messages_topic_id=direct_messages_topic_id,
            media=media,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters,
        )

    async def reply_media_group(
        self,
        media: Union[List[InputMediaAudio], List[InputMediaDocument], List[InputMediaLivePhoto], List[InputMediaPhoto], List[InputMediaVideo]],
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        reply_parameters: Optional[ReplyParameters] = None,
    ) -> List[Message]:
        """Как bot.send_media_group(), но чат берётся из апдейта, сообщение цитирует сообщение апдейта.
        
        Use this method to send a group of photos, live photos, videos, documents or audios as an album. Documents and audio files can be only grouped in an album with messages of the same type. On success, an Array of Message objects that were sent is returned.
        
        https://core.telegram.org/bots/api#sendmediagroup
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
            message_thread_id: Unique identifier for the target message thread (topic) of a forum; for forum supergroups and private chats of bots with forum topic mode enabled only
            direct_messages_topic_id: Identifier of the direct messages topic to which the messages will be sent; required if the messages are sent to a direct messages chat
            media: A JSON-serialized Array describing messages to be sent, must include 2-10 items
            disable_notification: Sends messages silently. Users will receive a notification with no sound.
            protect_content: Protects the contents of the sent messages from forwarding and saving
            allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance.
            message_effect_id: Unique identifier of the message effect to be added to the message; for private chats only
            reply_parameters: Description of the message to reply to
        """
        return await self.bot.send_media_group(
            business_connection_id=self._or_default("business_connection_id", business_connection_id),
            chat_id=self.chat_id,
            message_thread_id=self._or_default("message_thread_id", message_thread_id),
            direct_messages_topic_id=direct_messages_topic_id,
            media=media,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters if reply_parameters is not None else self._reply_parameters(),
        )

    async def answer_location(
        self,
        latitude: float,
        longitude: float,
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        horizontal_accuracy: Optional[float] = None,
        live_period: Optional[int] = None,
        heading: Optional[int] = None,
        proximity_alert_radius: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_location(), но чат берётся из апдейта.
        
        Use this method to send point on the map. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendlocation
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
            message_thread_id: Unique identifier for the target message thread (topic) of a forum; for forum supergroups and private chats of bots with forum topic mode enabled only
            direct_messages_topic_id: Identifier of the direct messages topic to which the message will be sent; required if the message is sent to a direct messages chat
            ephemeral_message_parameters: A JSON-serialized object containing the parameters of the ephemeral message to send
            latitude: Latitude of the location
            longitude: Longitude of the location
            horizontal_accuracy: The radius of uncertainty for the location, measured in meters; 0-1500
            live_period: Period in seconds during which the location will be updated (see Live Locations), must be between 60 and 86400, or 0x7FFFFFFF for live locations that can be edited indefinitely. Must be 0 for ephemeral messages.
            heading: For live locations, a direction in which the user is moving, in degrees. Must be between 1 and 360 if specified.
            proximity_alert_radius: For live locations, a maximum distance for proximity alerts about approaching another chat member, in meters. Must be between 1 and 100000 if specified.
            disable_notification: Sends the message silently. Users will receive a notification with no sound.
            protect_content: Protects the contents of the sent message from forwarding and saving
            allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance.
            message_effect_id: Unique identifier of the message effect to be added to the message; for private chats only
            suggested_post_parameters: A JSON-serialized object containing the parameters of the suggested post to send; for direct messages chats only. If the message is sent as a reply to another suggested post, then that suggested post is automatically declined.
            reply_parameters: Description of the message to reply to
            reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user.
        """
        return await self.bot.send_location(
            business_connection_id=self._or_default("business_connection_id", business_connection_id),
            chat_id=self.chat_id,
            message_thread_id=self._or_default("message_thread_id", message_thread_id),
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            latitude=latitude,
            longitude=longitude,
            horizontal_accuracy=horizontal_accuracy,
            live_period=live_period,
            heading=heading,
            proximity_alert_radius=proximity_alert_radius,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def reply_location(
        self,
        latitude: float,
        longitude: float,
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        horizontal_accuracy: Optional[float] = None,
        live_period: Optional[int] = None,
        heading: Optional[int] = None,
        proximity_alert_radius: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_location(), но чат берётся из апдейта, сообщение цитирует сообщение апдейта.
        
        Use this method to send point on the map. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendlocation
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
            message_thread_id: Unique identifier for the target message thread (topic) of a forum; for forum supergroups and private chats of bots with forum topic mode enabled only
            direct_messages_topic_id: Identifier of the direct messages topic to which the message will be sent; required if the message is sent to a direct messages chat
            ephemeral_message_parameters: A JSON-serialized object containing the parameters of the ephemeral message to send
            latitude: Latitude of the location
            longitude: Longitude of the location
            horizontal_accuracy: The radius of uncertainty for the location, measured in meters; 0-1500
            live_period: Period in seconds during which the location will be updated (see Live Locations), must be between 60 and 86400, or 0x7FFFFFFF for live locations that can be edited indefinitely. Must be 0 for ephemeral messages.
            heading: For live locations, a direction in which the user is moving, in degrees. Must be between 1 and 360 if specified.
            proximity_alert_radius: For live locations, a maximum distance for proximity alerts about approaching another chat member, in meters. Must be between 1 and 100000 if specified.
            disable_notification: Sends the message silently. Users will receive a notification with no sound.
            protect_content: Protects the contents of the sent message from forwarding and saving
            allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance.
            message_effect_id: Unique identifier of the message effect to be added to the message; for private chats only
            suggested_post_parameters: A JSON-serialized object containing the parameters of the suggested post to send; for direct messages chats only. If the message is sent as a reply to another suggested post, then that suggested post is automatically declined.
            reply_parameters: Description of the message to reply to
            reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user.
        """
        return await self.bot.send_location(
            business_connection_id=self._or_default("business_connection_id", business_connection_id),
            chat_id=self.chat_id,
            message_thread_id=self._or_default("message_thread_id", message_thread_id),
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            latitude=latitude,
            longitude=longitude,
            horizontal_accuracy=horizontal_accuracy,
            live_period=live_period,
            heading=heading,
            proximity_alert_radius=proximity_alert_radius,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters if reply_parameters is not None else self._reply_parameters(),
            reply_markup=reply_markup,
        )

    async def answer_venue(
        self,
        latitude: float,
        longitude: float,
        title: str,
        address: str,
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        foursquare_id: Optional[str] = None,
        foursquare_type: Optional[str] = None,
        google_place_id: Optional[str] = None,
        google_place_type: Optional[str] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_venue(), но чат берётся из апдейта.
        
        Use this method to send information about a venue. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendvenue
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
            message_thread_id: Unique identifier for the target message thread (topic) of a forum; for forum supergroups and private chats of bots with forum topic mode enabled only
            direct_messages_topic_id: Identifier of the direct messages topic to which the message will be sent; required if the message is sent to a direct messages chat
            ephemeral_message_parameters: A JSON-serialized object containing the parameters of the ephemeral message to send
            latitude: Latitude of the venue
            longitude: Longitude of the venue
            title: Name of the venue
            address: Address of the venue
            foursquare_id: Foursquare identifier of the venue
            foursquare_type: Foursquare type of the venue, if known. (For example, "arts_entertainment/default", "arts_entertainment/aquarium" or "food/icecream".)
            google_place_id: Google Places identifier of the venue
            google_place_type: Google Places type of the venue. (See supported types.)
            disable_notification: Sends the message silently. Users will receive a notification with no sound.
            protect_content: Protects the contents of the sent message from forwarding and saving
            allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance.
            message_effect_id: Unique identifier of the message effect to be added to the message; for private chats only
            suggested_post_parameters: A JSON-serialized object containing the parameters of the suggested post to send; for direct messages chats only. If the message is sent as a reply to another suggested post, then that suggested post is automatically declined.
            reply_parameters: Description of the message to reply to
            reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user.
        """
        return await self.bot.send_venue(
            business_connection_id=self._or_default("business_connection_id", business_connection_id),
            chat_id=self.chat_id,
            message_thread_id=self._or_default("message_thread_id", message_thread_id),
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            latitude=latitude,
            longitude=longitude,
            title=title,
            address=address,
            foursquare_id=foursquare_id,
            foursquare_type=foursquare_type,
            google_place_id=google_place_id,
            google_place_type=google_place_type,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def reply_venue(
        self,
        latitude: float,
        longitude: float,
        title: str,
        address: str,
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        foursquare_id: Optional[str] = None,
        foursquare_type: Optional[str] = None,
        google_place_id: Optional[str] = None,
        google_place_type: Optional[str] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_venue(), но чат берётся из апдейта, сообщение цитирует сообщение апдейта.
        
        Use this method to send information about a venue. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendvenue
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
            message_thread_id: Unique identifier for the target message thread (topic) of a forum; for forum supergroups and private chats of bots with forum topic mode enabled only
            direct_messages_topic_id: Identifier of the direct messages topic to which the message will be sent; required if the message is sent to a direct messages chat
            ephemeral_message_parameters: A JSON-serialized object containing the parameters of the ephemeral message to send
            latitude: Latitude of the venue
            longitude: Longitude of the venue
            title: Name of the venue
            address: Address of the venue
            foursquare_id: Foursquare identifier of the venue
            foursquare_type: Foursquare type of the venue, if known. (For example, "arts_entertainment/default", "arts_entertainment/aquarium" or "food/icecream".)
            google_place_id: Google Places identifier of the venue
            google_place_type: Google Places type of the venue. (See supported types.)
            disable_notification: Sends the message silently. Users will receive a notification with no sound.
            protect_content: Protects the contents of the sent message from forwarding and saving
            allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance.
            message_effect_id: Unique identifier of the message effect to be added to the message; for private chats only
            suggested_post_parameters: A JSON-serialized object containing the parameters of the suggested post to send; for direct messages chats only. If the message is sent as a reply to another suggested post, then that suggested post is automatically declined.
            reply_parameters: Description of the message to reply to
            reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user.
        """
        return await self.bot.send_venue(
            business_connection_id=self._or_default("business_connection_id", business_connection_id),
            chat_id=self.chat_id,
            message_thread_id=self._or_default("message_thread_id", message_thread_id),
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            latitude=latitude,
            longitude=longitude,
            title=title,
            address=address,
            foursquare_id=foursquare_id,
            foursquare_type=foursquare_type,
            google_place_id=google_place_id,
            google_place_type=google_place_type,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters if reply_parameters is not None else self._reply_parameters(),
            reply_markup=reply_markup,
        )

    async def answer_contact(
        self,
        phone_number: str,
        first_name: str,
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        last_name: Optional[str] = None,
        vcard: Optional[str] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_contact(), но чат берётся из апдейта.
        
        Use this method to send phone contacts. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendcontact
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
            message_thread_id: Unique identifier for the target message thread (topic) of a forum; for forum supergroups and private chats of bots with forum topic mode enabled only
            direct_messages_topic_id: Identifier of the direct messages topic to which the message will be sent; required if the message is sent to a direct messages chat
            ephemeral_message_parameters: A JSON-serialized object containing the parameters of the ephemeral message to send
            phone_number: Contact's phone number
            first_name: Contact's first name
            last_name: Contact's last name
            vcard: Additional data about the contact in the form of a vCard, 0-2048 bytes
            disable_notification: Sends the message silently. Users will receive a notification with no sound.
            protect_content: Protects the contents of the sent message from forwarding and saving
            allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance.
            message_effect_id: Unique identifier of the message effect to be added to the message; for private chats only
            suggested_post_parameters: A JSON-serialized object containing the parameters of the suggested post to send; for direct messages chats only. If the message is sent as a reply to another suggested post, then that suggested post is automatically declined.
            reply_parameters: Description of the message to reply to
            reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user.
        """
        return await self.bot.send_contact(
            business_connection_id=self._or_default("business_connection_id", business_connection_id),
            chat_id=self.chat_id,
            message_thread_id=self._or_default("message_thread_id", message_thread_id),
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            vcard=vcard,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def reply_contact(
        self,
        phone_number: str,
        first_name: str,
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        last_name: Optional[str] = None,
        vcard: Optional[str] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_contact(), но чат берётся из апдейта, сообщение цитирует сообщение апдейта.
        
        Use this method to send phone contacts. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendcontact
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
            message_thread_id: Unique identifier for the target message thread (topic) of a forum; for forum supergroups and private chats of bots with forum topic mode enabled only
            direct_messages_topic_id: Identifier of the direct messages topic to which the message will be sent; required if the message is sent to a direct messages chat
            ephemeral_message_parameters: A JSON-serialized object containing the parameters of the ephemeral message to send
            phone_number: Contact's phone number
            first_name: Contact's first name
            last_name: Contact's last name
            vcard: Additional data about the contact in the form of a vCard, 0-2048 bytes
            disable_notification: Sends the message silently. Users will receive a notification with no sound.
            protect_content: Protects the contents of the sent message from forwarding and saving
            allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance.
            message_effect_id: Unique identifier of the message effect to be added to the message; for private chats only
            suggested_post_parameters: A JSON-serialized object containing the parameters of the suggested post to send; for direct messages chats only. If the message is sent as a reply to another suggested post, then that suggested post is automatically declined.
            reply_parameters: Description of the message to reply to
            reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user.
        """
        return await self.bot.send_contact(
            business_connection_id=self._or_default("business_connection_id", business_connection_id),
            chat_id=self.chat_id,
            message_thread_id=self._or_default("message_thread_id", message_thread_id),
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            vcard=vcard,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters if reply_parameters is not None else self._reply_parameters(),
            reply_markup=reply_markup,
        )

    async def answer_poll(
        self,
        question: str,
        options: List[InputPollOption],
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        question_parse_mode: Optional[str] = None,
        question_entities: Optional[List[MessageEntity]] = None,
        is_anonymous: Optional[bool] = None,
        type: Optional[str] = None,
        allows_multiple_answers: Optional[bool] = None,
        allows_revoting: Optional[bool] = None,
        shuffle_options: Optional[bool] = None,
        allow_adding_options: Optional[bool] = None,
        hide_results_until_closes: Optional[bool] = None,
        members_only: Optional[bool] = None,
        country_codes: Optional[List[str]] = None,
        correct_option_ids: Optional[List[int]] = None,
        explanation: Optional[str] = None,
        explanation_parse_mode: Optional[str] = None,
        explanation_entities: Optional[List[MessageEntity]] = None,
        explanation_media: Optional[InputPollMedia] = None,
        open_period: Optional[int] = None,
        close_date: Optional[int] = None,
        is_closed: Optional[bool] = None,
        description: Optional[str] = None,
        description_parse_mode: Optional[str] = None,
        description_entities: Optional[List[MessageEntity]] = None,
        media: Optional[InputPollMedia] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_poll(), но чат берётся из апдейта.
        
        Use this method to send a native poll. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendpoll
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
            message_thread_id: Unique identifier for the target message thread (topic) of a forum; for forum supergroups and private chats of bots with forum topic mode enabled only
            question: Poll question, 1-300 characters
            question_parse_mode: Mode for parsing entities in the question. See formatting options for more details. Currently, only custom emoji entities are allowed.
            question_entities: A JSON-serialized list of special entities that appear in the poll question. It can be specified instead of question_parse_mode.
            options: A JSON-serialized list of 1-12 answer options
            is_anonymous: True, if the poll needs to be anonymous, defaults to True
            type: Poll type, "quiz" or "regular", defaults to "regular"
            allows_multiple_answers: Pass True if the poll allows multiple answers, defaults to False
            allows_revoting: Pass True if the poll allows to change chosen answer options, defaults to False for quizzes and to True for regular polls
            shuffle_options: Pass True if the poll options must be shown in random order
            allow_adding_options: Pass True if answer options can be added to the poll after creation; not supported for anonymous polls and quizzes
            hide_results_until_closes: Pass True if poll results must be shown only after the poll closes
            members_only: Pass True if voting is limited to users who have been members of the chat where the poll is being sent for more than 24 hours; for channel chats only
            country_codes: A JSON-serialized list of 0-12 two-letter ISO 3166-1 alpha-2 country codes indicating the countries from which users can vote in the poll; for channel chats only. Use "FT" as a country code to allow users with anonymous numbers to vote. If omitted or empty, then users from any country can participate in the poll.
            correct_option_ids: A JSON-serialized list of monotonically increasing 0-based identifiers of the correct answer options, required for polls in quiz mode
            explanation: Text that is shown when a user chooses an incorrect answer or taps on the lamp icon in a quiz-style poll, 0-200 characters with at most 2 line feeds after entities parsing
            explanation_parse_mode: Mode for parsing entities in the explanation. See formatting options for more details.
            explanation_entities: A JSON-serialized list of special entities that appear in the poll explanation. It can be specified instead of explanation_parse_mode.
            explanation_media: Media added to the quiz explanation
            open_period: Amount of time in seconds the poll will be active after creation, 5-2628000. Can't be used together with close_date.
            close_date: Point in time (Unix timestamp) when the poll will be automatically closed. Must be at least 5 and no more than 2628000 seconds in the future. Can't be used together with open_period.
            is_closed: Pass True if the poll needs to be immediately closed. This can be useful for poll preview.
            description: Description of the poll to be sent, 0-1024 characters after entities parsing
            description_parse_mode: Mode for parsing entities in the poll description. See formatting options for more details.
            description_entities: A JSON-serialized list of special entities that appear in the poll description, which can be specified instead of description_parse_mode
            media: Media added to the poll description
            disable_notification: Sends the message silently. Users will receive a notification with no sound.
            protect_content: Protects the contents of the sent message from forwarding and saving
            allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance.
            message_effect_id: Unique identifier of the message effect to be added to the message; for private chats only
            reply_parameters: Description of the message to reply to
            reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user.
        """
        return await self.bot.send_poll(
            business_connection_id=self._or_default("business_connection_id", business_connection_id),
            chat_id=self.chat_id,
            message_thread_id=self._or_default("message_thread_id", message_thread_id),
            question=question,
            question_parse_mode=question_parse_mode,
            question_entities=question_entities,
            options=options,
            is_anonymous=is_anonymous,
            type=type,
            allows_multiple_answers=allows_multiple_answers,
            allows_revoting=allows_revoting,
            shuffle_options=shuffle_options,
            allow_adding_options=allow_adding_options,
            hide_results_until_closes=hide_results_until_closes,
            members_only=members_only,
            country_codes=country_codes,
            correct_option_ids=correct_option_ids,
            explanation=explanation,
            explanation_parse_mode=explanation_parse_mode,
            explanation_entities=explanation_entities,
            explanation_media=explanation_media,
            open_period=open_period,
            close_date=close_date,
            is_closed=is_closed,
            description=description,
            description_parse_mode=description_parse_mode,
            description_entities=description_entities,
            media=media,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def reply_poll(
        self,
        question: str,
        options: List[InputPollOption],
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        question_parse_mode: Optional[str] = None,
        question_entities: Optional[List[MessageEntity]] = None,
        is_anonymous: Optional[bool] = None,
        type: Optional[str] = None,
        allows_multiple_answers: Optional[bool] = None,
        allows_revoting: Optional[bool] = None,
        shuffle_options: Optional[bool] = None,
        allow_adding_options: Optional[bool] = None,
        hide_results_until_closes: Optional[bool] = None,
        members_only: Optional[bool] = None,
        country_codes: Optional[List[str]] = None,
        correct_option_ids: Optional[List[int]] = None,
        explanation: Optional[str] = None,
        explanation_parse_mode: Optional[str] = None,
        explanation_entities: Optional[List[MessageEntity]] = None,
        explanation_media: Optional[InputPollMedia] = None,
        open_period: Optional[int] = None,
        close_date: Optional[int] = None,
        is_closed: Optional[bool] = None,
        description: Optional[str] = None,
        description_parse_mode: Optional[str] = None,
        description_entities: Optional[List[MessageEntity]] = None,
        media: Optional[InputPollMedia] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_poll(), но чат берётся из апдейта, сообщение цитирует сообщение апдейта.
        
        Use this method to send a native poll. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendpoll
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
            message_thread_id: Unique identifier for the target message thread (topic) of a forum; for forum supergroups and private chats of bots with forum topic mode enabled only
            question: Poll question, 1-300 characters
            question_parse_mode: Mode for parsing entities in the question. See formatting options for more details. Currently, only custom emoji entities are allowed.
            question_entities: A JSON-serialized list of special entities that appear in the poll question. It can be specified instead of question_parse_mode.
            options: A JSON-serialized list of 1-12 answer options
            is_anonymous: True, if the poll needs to be anonymous, defaults to True
            type: Poll type, "quiz" or "regular", defaults to "regular"
            allows_multiple_answers: Pass True if the poll allows multiple answers, defaults to False
            allows_revoting: Pass True if the poll allows to change chosen answer options, defaults to False for quizzes and to True for regular polls
            shuffle_options: Pass True if the poll options must be shown in random order
            allow_adding_options: Pass True if answer options can be added to the poll after creation; not supported for anonymous polls and quizzes
            hide_results_until_closes: Pass True if poll results must be shown only after the poll closes
            members_only: Pass True if voting is limited to users who have been members of the chat where the poll is being sent for more than 24 hours; for channel chats only
            country_codes: A JSON-serialized list of 0-12 two-letter ISO 3166-1 alpha-2 country codes indicating the countries from which users can vote in the poll; for channel chats only. Use "FT" as a country code to allow users with anonymous numbers to vote. If omitted or empty, then users from any country can participate in the poll.
            correct_option_ids: A JSON-serialized list of monotonically increasing 0-based identifiers of the correct answer options, required for polls in quiz mode
            explanation: Text that is shown when a user chooses an incorrect answer or taps on the lamp icon in a quiz-style poll, 0-200 characters with at most 2 line feeds after entities parsing
            explanation_parse_mode: Mode for parsing entities in the explanation. See formatting options for more details.
            explanation_entities: A JSON-serialized list of special entities that appear in the poll explanation. It can be specified instead of explanation_parse_mode.
            explanation_media: Media added to the quiz explanation
            open_period: Amount of time in seconds the poll will be active after creation, 5-2628000. Can't be used together with close_date.
            close_date: Point in time (Unix timestamp) when the poll will be automatically closed. Must be at least 5 and no more than 2628000 seconds in the future. Can't be used together with open_period.
            is_closed: Pass True if the poll needs to be immediately closed. This can be useful for poll preview.
            description: Description of the poll to be sent, 0-1024 characters after entities parsing
            description_parse_mode: Mode for parsing entities in the poll description. See formatting options for more details.
            description_entities: A JSON-serialized list of special entities that appear in the poll description, which can be specified instead of description_parse_mode
            media: Media added to the poll description
            disable_notification: Sends the message silently. Users will receive a notification with no sound.
            protect_content: Protects the contents of the sent message from forwarding and saving
            allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance.
            message_effect_id: Unique identifier of the message effect to be added to the message; for private chats only
            reply_parameters: Description of the message to reply to
            reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user.
        """
        return await self.bot.send_poll(
            business_connection_id=self._or_default("business_connection_id", business_connection_id),
            chat_id=self.chat_id,
            message_thread_id=self._or_default("message_thread_id", message_thread_id),
            question=question,
            question_parse_mode=question_parse_mode,
            question_entities=question_entities,
            options=options,
            is_anonymous=is_anonymous,
            type=type,
            allows_multiple_answers=allows_multiple_answers,
            allows_revoting=allows_revoting,
            shuffle_options=shuffle_options,
            allow_adding_options=allow_adding_options,
            hide_results_until_closes=hide_results_until_closes,
            members_only=members_only,
            country_codes=country_codes,
            correct_option_ids=correct_option_ids,
            explanation=explanation,
            explanation_parse_mode=explanation_parse_mode,
            explanation_entities=explanation_entities,
            explanation_media=explanation_media,
            open_period=open_period,
            close_date=close_date,
            is_closed=is_closed,
            description=description,
            description_parse_mode=description_parse_mode,
            description_entities=description_entities,
            media=media,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters if reply_parameters is not None else self._reply_parameters(),
            reply_markup=reply_markup,
        )

    async def answer_checklist(
        self,
        business_connection_id: str,
        checklist: InputChecklist,
        *,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ) -> Message:
        """Как bot.send_checklist(), но чат берётся из апдейта.
        
        Use this method to send a checklist on behalf of a connected business account. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendchecklist
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
            checklist: A JSON-serialized object for the checklist to send
            disable_notification: Sends the message silently. Users will receive a notification with no sound.
            protect_content: Protects the contents of the sent message from forwarding and saving
            message_effect_id: Unique identifier of the message effect to be added to the message
            reply_parameters: A JSON-serialized object for description of the message to reply to
            reply_markup: A JSON-serialized object for an inline keyboard
        """
        return await self.bot.send_checklist(
            business_connection_id=self._or_default("business_connection_id", business_connection_id),
            chat_id=self.chat_id,
            checklist=checklist,
            disable_notification=disable_notification,
            protect_content=protect_content,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def reply_checklist(
        self,
        business_connection_id: str,
        checklist: InputChecklist,
        *,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ) -> Message:
        """Как bot.send_checklist(), но чат берётся из апдейта, сообщение цитирует сообщение апдейта.
        
        Use this method to send a checklist on behalf of a connected business account. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendchecklist
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
            checklist: A JSON-serialized object for the checklist to send
            disable_notification: Sends the message silently. Users will receive a notification with no sound.
            protect_content: Protects the contents of the sent message from forwarding and saving
            message_effect_id: Unique identifier of the message effect to be added to the message
            reply_parameters: A JSON-serialized object for description of the message to reply to
            reply_markup: A JSON-serialized object for an inline keyboard
        """
        return await self.bot.send_checklist(
            business_connection_id=self._or_default("business_connection_id", business_connection_id),
            chat_id=self.chat_id,
            checklist=checklist,
            disable_notification=disable_notification,
            protect_content=protect_content,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters if reply_parameters is not None else self._reply_parameters(),
            reply_markup=reply_markup,
        )

    async def answer_dice(
        self,
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        emoji: Optional[str] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_dice(), но чат берётся из апдейта.
        
        Use this method to send an animated emoji that will display a random value. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#senddice
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
            message_thread_id: Unique identifier for the target message thread (topic) of a forum; for forum supergroups and private chats of bots with forum topic mode enabled only
            direct_messages_topic_id: Identifier of the direct messages topic to which the message will be sent; required if the message is sent to a direct messages chat
            emoji: Emoji on which the dice throw animation is based. Currently, must be one of "🎲", "🎯", "🏀", "⚽", "🎳", or "🎰". Dice can have values 1-6 for "🎲", "🎯" and "🎳", values 1-5 for "🏀" and "⚽", and values 1-64 for "🎰". Defaults to "🎲".
            disable_notification: Sends the message silently. Users will receive a notification with no sound.
            protect_content: Protects the contents of the sent message from forwarding
            allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance.
            message_effect_id: Unique identifier of the message effect to be added to the message; for private chats only
            suggested_post_parameters: A JSON-serialized object containing the parameters of the suggested post to send; for direct messages chats only. If the message is sent as a reply to another suggested post, then that suggested post is automatically declined.
            reply_parameters: Description of the message to reply to
            reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user.
        """
        return await self.bot.send_dice(
            business_connection_id=self._or_default("business_connection_id", business_connection_id),
            chat_id=self.chat_id,
            message_thread_id=self._or_default("message_thread_id", message_thread_id),
            direct_messages_topic_id=direct_messages_topic_id,
            emoji=emoji,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def reply_dice(
        self,
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        emoji: Optional[str] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_dice(), но чат берётся из апдейта, сообщение цитирует сообщение апдейта.
        
        Use this method to send an animated emoji that will display a random value. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#senddice
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
            message_thread_id: Unique identifier for the target message thread (topic) of a forum; for forum supergroups and private chats of bots with forum topic mode enabled only
            direct_messages_topic_id: Identifier of the direct messages topic to which the message will be sent; required if the message is sent to a direct messages chat
            emoji: Emoji on which the dice throw animation is based. Currently, must be one of "🎲", "🎯", "🏀", "⚽", "🎳", or "🎰". Dice can have values 1-6 for "🎲", "🎯" and "🎳", values 1-5 for "🏀" and "⚽", and values 1-64 for "🎰". Defaults to "🎲".
            disable_notification: Sends the message silently. Users will receive a notification with no sound.
            protect_content: Protects the contents of the sent message from forwarding
            allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance.
            message_effect_id: Unique identifier of the message effect to be added to the message; for private chats only
            suggested_post_parameters: A JSON-serialized object containing the parameters of the suggested post to send; for direct messages chats only. If the message is sent as a reply to another suggested post, then that suggested post is automatically declined.
            reply_parameters: Description of the message to reply to
            reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user.
        """
        return await self.bot.send_dice(
            business_connection_id=self._or_default("business_connection_id", business_connection_id),
            chat_id=self.chat_id,
            message_thread_id=self._or_default("message_thread_id", message_thread_id),
            direct_messages_topic_id=direct_messages_topic_id,
            emoji=emoji,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters if reply_parameters is not None else self._reply_parameters(),
            reply_markup=reply_markup,
        )

    async def answer_message_draft(
        self,
        draft_id: int,
        *,
        message_thread_id: Optional[int] = None,
        text: Optional[str] = None,
        parse_mode: Optional[str] = None,
        entities: Optional[List[MessageEntity]] = None,
        can_stop: Optional[bool] = None,
        keep_on_stop: Optional[bool] = None,
    ) -> bool:
        """Как bot.send_message_draft(), но чат берётся из апдейта.
        
        Use this method to stream a partial message to a user while the message is being generated. Note that the streamed draft is ephemeral and acts as a temporary 30-second preview - once the output is finalized, you must call sendMessage with the complete message to persist it in the user's chat. Returns True on success.
        
        https://core.telegram.org/bots/api#sendmessagedraft
        
        Args:
            message_thread_id: Unique identifier for the target message thread
            draft_id: Unique identifier of the message draft; must be non-zero. Changes to drafts with the same identifier are animated. Otherwise, the draft is replaced without animation.
            text: Text of the message to be sent, 0-4096 characters after entities parsing. Pass an empty text to show a "Thinking..." placeholder.
            parse_mode: Mode for parsing entities in the message text. See formatting options for more details.
            entities: A JSON-serialized list of special entities that appear in message text, which can be specified instead of parse_mode
            can_stop: Pass True to show the user a button to stop further drafts. The bot will receive an Update "stopped_message_generation" if the user presses the button.
            keep_on_stop: Pass True to keep the draft in the chat when the button is pressed. The draft will still disappear after a short time or if the bot sends a message. To fully preserve the partial draft, the bot should send it as a new message.
        """
        return await self.bot.send_message_draft(
            chat_id=self.chat_id,
            message_thread_id=self._or_default("message_thread_id", message_thread_id),
            draft_id=draft_id,
            text=text,
            parse_mode=parse_mode,
            entities=entities,
            can_stop=can_stop,
            keep_on_stop=keep_on_stop,
        )

    async def answer_chat_action(
        self,
        action: str,
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
    ) -> bool:
        """Как bot.send_chat_action(), но чат берётся из апдейта.
        
        Use this method when you need to tell the user that something is happening on the bot's side. The status is set for 5 seconds or less (when a message arrives from your bot, Telegram clients clear its typing status). Returns True on success.
        
        We only recommend using this method when a response from the bot will take a noticeable amount of time to arrive.
        
        https://core.telegram.org/bots/api#sendchataction
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the action will be sent
            message_thread_id: Unique identifier for the target message thread or topic of a forum; for supergroups and private chats of bots with forum topic mode enabled only
            action: Type of action to broadcast. Choose one, depending on what the user is about to receive: typing for text messages, upload_photo for photos, record_video or upload_video for videos, record_voice or upload_voice for voice notes, upload_document for general files, choose_sticker for stickers, find_location for location data, record_video_note or upload_video_note for video notes.
        """
        return await self.bot.send_chat_action(
            business_connection_id=self._or_default("business_connection_id", business_connection_id),
            chat_id=self.chat_id,
            message_thread_id=self._or_default("message_thread_id", message_thread_id),
            action=action,
        )

    async def set_message_reaction(
        self,
        *,
        message_id: Optional[int] = None,
        reaction: Optional[List[ReactionType]] = None,
        is_big: Optional[bool] = None,
    ) -> bool:
        """Как bot.set_message_reaction(), но chat_id берётся из апдейта.
        
        Use this method to change the chosen reactions on a message. Service messages of some types can't be reacted to. Automatically forwarded messages from a channel to its discussion group have the same available reactions as messages in the channel. Bots can't use paid reactions. Returns True on success.
        
        https://core.telegram.org/bots/api#setmessagereaction
        
        Args:
            message_id: Identifier of the target message. If the message belongs to a media group, the reaction is set to the first non-deleted message in the group instead.
            reaction: A JSON-serialized list of reaction types to set on the message. Currently, as non-premium users, bots can set up to one reaction per message. A custom emoji reaction can be used if it is either already present on the message or explicitly allowed by chat administrators. Paid reactions can't be used by bots.
            is_big: Pass True to set the reaction with a big animation
        """
        return await self.bot.set_message_reaction(
            chat_id=self.chat_id,
            message_id=message_id if message_id is not None else self._require_message_id(),
            reaction=reaction,
            is_big=is_big,
        )

    async def ban_chat_member(
        self,
        user_id: int,
        *,
        until_date: Optional[int] = None,
        revoke_messages: Optional[bool] = None,
    ) -> bool:
        """Как bot.ban_chat_member(), но chat_id берётся из апдейта.
        
        Use this method to ban a user in a group, a supergroup or a channel. In the case of supergroups and channels, the user will not be able to return to the chat on their own using invite links, etc., unless unbanned first. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Returns True on success.
        
        https://core.telegram.org/bots/api#banchatmember
        
        Args:
            user_id: Unique identifier of the target user
            until_date: Date when the user will be unbanned; Unix time. If user is banned for more than 366 days or less than 30 seconds from the current time they are considered to be banned forever. Applied for supergroups and channels only.
            revoke_messages: Pass True to delete all messages from the chat for the user that is being removed. If False, the user will be able to see messages in the group that were sent before the user was removed. Always True for supergroups and channels.
        """
        return await self.bot.ban_chat_member(
            chat_id=self.chat_id,
            user_id=user_id,
            until_date=until_date,
            revoke_messages=revoke_messages,
        )

    async def unban_chat_member(
        self,
        user_id: int,
        *,
        only_if_banned: Optional[bool] = None,
    ) -> bool:
        """Как bot.unban_chat_member(), но chat_id берётся из апдейта.
        
        Use this method to unban a previously banned user in a supergroup or channel. The user will not return to the group or channel automatically, but will be able to join via link, etc. The bot must be an administrator for this to work. By default, this method guarantees that after the call the user is not a member of the chat, but will be able to join it. So if the user is a member of the chat they will also be removed from the chat. If you don't want this, use the parameter only_if_banned. Returns True on success.
        
        https://core.telegram.org/bots/api#unbanchatmember
        
        Args:
            user_id: Unique identifier of the target user
            only_if_banned: Do nothing if the user is not banned
        """
        return await self.bot.unban_chat_member(
            chat_id=self.chat_id,
            user_id=user_id,
            only_if_banned=only_if_banned,
        )

    async def restrict_chat_member(
        self,
        user_id: int,
        permissions: ChatPermissions,
        *,
        use_independent_chat_permissions: Optional[bool] = None,
        until_date: Optional[int] = None,
    ) -> bool:
        """Как bot.restrict_chat_member(), но chat_id берётся из апдейта.
        
        Use this method to restrict a user in a supergroup. The bot must be an administrator in the supergroup for this to work and must have the appropriate administrator rights. Pass True for all permissions to lift restrictions from a user. Returns True on success.
        
        https://core.telegram.org/bots/api#restrictchatmember
        
        Args:
            user_id: Unique identifier of the target user
            permissions: A JSON-serialized object for new user permissions
            use_independent_chat_permissions: Pass True if chat permissions are set independently. Otherwise, the can_send_other_messages and can_add_web_page_previews permissions will imply the can_send_messages, can_send_audios, can_send_documents, can_send_photos, can_send_videos, can_send_video_notes, and can_send_voice_notes permissions; the can_send_polls permission will imply the can_send_messages permission.
            until_date: Date when restrictions will be lifted for the user; Unix time. If user is restricted for more than 366 days or less than 30 seconds from the current time, they are considered to be restricted forever.
        """
        return await self.bot.restrict_chat_member(
            chat_id=self.chat_id,
            user_id=user_id,
            permissions=permissions,
            use_independent_chat_permissions=use_independent_chat_permissions,
            until_date=until_date,
        )

    async def promote_chat_member(
        self,
        user_id: int,
        *,
        is_anonymous: Optional[bool] = None,
        can_manage_chat: Optional[bool] = None,
        can_delete_messages: Optional[bool] = None,
        can_manage_video_chats: Optional[bool] = None,
        can_restrict_members: Optional[bool] = None,
        can_promote_members: Optional[bool] = None,
        can_change_info: Optional[bool] = None,
        can_invite_users: Optional[bool] = None,
        can_post_stories: Optional[bool] = None,
        can_edit_stories: Optional[bool] = None,
        can_delete_stories: Optional[bool] = None,
        can_post_messages: Optional[bool] = None,
        can_edit_messages: Optional[bool] = None,
        can_pin_messages: Optional[bool] = None,
        can_manage_topics: Optional[bool] = None,
        can_manage_direct_messages: Optional[bool] = None,
        can_manage_tags: Optional[bool] = None,
        can_send_welcome_messages: Optional[bool] = None,
    ) -> bool:
        """Как bot.promote_chat_member(), но chat_id берётся из апдейта.
        
        Use this method to promote or demote a user in a supergroup or a channel. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Pass False for all boolean parameters to demote a user. Returns True on success.
        
        https://core.telegram.org/bots/api#promotechatmember
        
        Args:
            user_id: Unique identifier of the target user
            is_anonymous: Pass True if the administrator's presence in the chat is hidden
            can_manage_chat: Pass True if the administrator can access the chat event log, get boost list, see hidden supergroup and channel members, report spam messages, ignore slow mode, and send messages to the chat without paying Telegram Stars. Implied by any other administrator privilege.
            can_delete_messages: Pass True if the administrator can delete messages of other users
            can_manage_video_chats: Pass True if the administrator can manage video chats
            can_restrict_members: Pass True if the administrator can restrict, ban or unban chat members, or access supergroup statistics. For backward compatibility, defaults to True for promotions of channel administrators.
            can_promote_members: Pass True if the administrator can add new administrators with a subset of their own privileges or demote administrators that they have promoted, directly or indirectly (promoted by administrators that were appointed by him)
            can_change_info: Pass True if the administrator can change chat title, photo and other settings
            can_invite_users: Pass True if the administrator can invite new users to the chat
            can_post_stories: Pass True if the administrator can post stories to the chat
            can_edit_stories: Pass True if the administrator can edit stories posted by other users, post stories to the chat page, pin chat stories, and access the chat's story archive
            can_delete_stories: Pass True if the administrator can delete stories posted by other users
            can_post_messages: Pass True if the administrator can post messages in the channel, approve suggested posts, or access channel statistics; for channels only
            can_edit_messages: Pass True if the administrator can edit messages of other users and can pin messages; for channels only
            can_pin_messages: Pass True if the administrator can pin messages; for supergroups only
            can_manage_topics: Pass True if the user is allowed to create, rename, close, and reopen forum topics; for supergroups only
            can_manage_direct_messages: Pass True if the administrator can manage direct messages within the channel and decline suggested posts; for channels only
            can_manage_tags: Pass True if the administrator can edit the tags of regular members; for groups and supergroups only
            can_send_welcome_messages: Pass True if the administrator can manage chat welcome messages or directly send them in the case of bots
        """
        return await self.bot.promote_chat_member(
            chat_id=self.chat_id,
            user_id=user_id,
            is_anonymous=is_anonymous,
            can_manage_chat=can_manage_chat,
            can_delete_messages=can_delete_messages,
            can_manage_video_chats=can_manage_video_chats,
            can_restrict_members=can_restrict_members,
            can_promote_members=can_promote_members,
            can_change_info=can_change_info,
            can_invite_users=can_invite_users,
            can_post_stories=can_post_stories,
            can_edit_stories=can_edit_stories,
            can_delete_stories=can_delete_stories,
            can_post_messages=can_post_messages,
            can_edit_messages=can_edit_messages,
            can_pin_messages=can_pin_messages,
            can_manage_topics=can_manage_topics,
            can_manage_direct_messages=can_manage_direct_messages,
            can_manage_tags=can_manage_tags,
            can_send_welcome_messages=can_send_welcome_messages,
        )

    async def set_chat_administrator_custom_title(
        self,
        user_id: int,
        custom_title: str,
    ) -> bool:
        """Как bot.set_chat_administrator_custom_title(), но chat_id берётся из апдейта.
        
        Use this method to set a custom title for an administrator in a supergroup promoted by the bot. Returns True on success.
        
        https://core.telegram.org/bots/api#setchatadministratorcustomtitle
        
        Args:
            user_id: Unique identifier of the target user
            custom_title: New custom title for the administrator; 0-16 characters, emoji are not allowed
        """
        return await self.bot.set_chat_administrator_custom_title(
            chat_id=self.chat_id,
            user_id=user_id,
            custom_title=custom_title,
        )

    async def set_chat_member_tag(
        self,
        user_id: int,
        *,
        tag: Optional[str] = None,
    ) -> bool:
        """Как bot.set_chat_member_tag(), но chat_id берётся из апдейта.
        
        Use this method to set a tag for a regular member in a group or a supergroup. The bot must be an administrator in the chat for this to work and must have the can_manage_tags administrator right. Returns True on success.
        
        https://core.telegram.org/bots/api#setchatmembertag
        
        Args:
            user_id: Unique identifier of the target user
            tag: New tag for the member; 0-16 characters, emoji are not allowed
        """
        return await self.bot.set_chat_member_tag(
            chat_id=self.chat_id,
            user_id=user_id,
            tag=tag,
        )

    async def ban_chat_sender_chat(
        self,
        sender_chat_id: int,
    ) -> bool:
        """Как bot.ban_chat_sender_chat(), но chat_id берётся из апдейта.
        
        Use this method to ban a channel chat in a supergroup or a channel. Until the chat is unbanned, the owner of the banned chat won't be able to send messages on behalf of any of their channels. The bot must be an administrator in the supergroup or channel for this to work and must have the appropriate administrator rights. Returns True on success.
        
        https://core.telegram.org/bots/api#banchatsenderchat
        
        Args:
            sender_chat_id: Unique identifier of the target sender chat
        """
        return await self.bot.ban_chat_sender_chat(
            chat_id=self.chat_id,
            sender_chat_id=sender_chat_id,
        )

    async def unban_chat_sender_chat(
        self,
        sender_chat_id: int,
    ) -> bool:
        """Как bot.unban_chat_sender_chat(), но chat_id берётся из апдейта.
        
        Use this method to unban a previously banned channel chat in a supergroup or channel. The bot must be an administrator for this to work and must have the appropriate administrator rights. Returns True on success.
        
        https://core.telegram.org/bots/api#unbanchatsenderchat
        
        Args:
            sender_chat_id: Unique identifier of the target sender chat
        """
        return await self.bot.unban_chat_sender_chat(
            chat_id=self.chat_id,
            sender_chat_id=sender_chat_id,
        )

    async def set_chat_permissions(
        self,
        permissions: ChatPermissions,
        *,
        use_independent_chat_permissions: Optional[bool] = None,
    ) -> bool:
        """Как bot.set_chat_permissions(), но chat_id берётся из апдейта.
        
        Use this method to set default chat permissions for all members. The bot must be an administrator in the group or a supergroup for this to work and must have the can_restrict_members administrator rights. Returns True on success.
        
        https://core.telegram.org/bots/api#setchatpermissions
        
        Args:
            permissions: A JSON-serialized object for new default chat permissions
            use_independent_chat_permissions: Pass True if chat permissions are set independently. Otherwise, the can_send_other_messages and can_add_web_page_previews permissions will imply the can_send_messages, can_send_audios, can_send_documents, can_send_photos, can_send_videos, can_send_video_notes, and can_send_voice_notes permissions; the can_send_polls permission will imply the can_send_messages permission.
        """
        return await self.bot.set_chat_permissions(
            chat_id=self.chat_id,
            permissions=permissions,
            use_independent_chat_permissions=use_independent_chat_permissions,
        )

    async def export_chat_invite_link(
        self,
    ) -> str:
        """Как bot.export_chat_invite_link(), но chat_id берётся из апдейта.
        
        Use this method to generate a new primary invite link for a chat; any previously generated primary link is revoked. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Returns the new invite link as String on success.
        
        https://core.telegram.org/bots/api#exportchatinvitelink
        """
        return await self.bot.export_chat_invite_link(
            chat_id=self.chat_id,
        )

    async def create_chat_invite_link(
        self,
        *,
        name: Optional[str] = None,
        expire_date: Optional[int] = None,
        member_limit: Optional[int] = None,
        creates_join_request: Optional[bool] = None,
    ) -> ChatInviteLink:
        """Как bot.create_chat_invite_link(), но chat_id берётся из апдейта.
        
        Use this method to create an additional invite link for a chat. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. The link can be revoked using the method revokeChatInviteLink. Returns the new invite link as ChatInviteLink object.
        
        https://core.telegram.org/bots/api#createchatinvitelink
        
        Args:
            name: Invite link name; 0-32 characters
            expire_date: Point in time (Unix timestamp) when the link will expire
            member_limit: The maximum number of users that can be members of the chat simultaneously after joining the chat via this invite link; 1-99999
            creates_join_request: True, if users joining the chat via the link need to be approved by chat administrators. If True, member_limit can't be specified.
        """
        return await self.bot.create_chat_invite_link(
            chat_id=self.chat_id,
            name=name,
            expire_date=expire_date,
            member_limit=member_limit,
            creates_join_request=creates_join_request,
        )

    async def edit_chat_invite_link(
        self,
        invite_link: str,
        *,
        name: Optional[str] = None,
        expire_date: Optional[int] = None,
        member_limit: Optional[int] = None,
        creates_join_request: Optional[bool] = None,
    ) -> ChatInviteLink:
        """Как bot.edit_chat_invite_link(), но chat_id берётся из апдейта.
        
        Use this method to edit a non-primary invite link created by the bot. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Returns the edited invite link as a ChatInviteLink object.
        
        https://core.telegram.org/bots/api#editchatinvitelink
        
        Args:
            invite_link: The invite link to edit
            name: Invite link name; 0-32 characters
            expire_date: Point in time (Unix timestamp) when the link will expire
            member_limit: The maximum number of users that can be members of the chat simultaneously after joining the chat via this invite link; 1-99999
            creates_join_request: True, if users joining the chat via the link need to be approved by chat administrators. If True, member_limit can't be specified.
        """
        return await self.bot.edit_chat_invite_link(
            chat_id=self.chat_id,
            invite_link=invite_link,
            name=name,
            expire_date=expire_date,
            member_limit=member_limit,
            creates_join_request=creates_join_request,
        )

    async def create_chat_subscription_invite_link(
        self,
        subscription_period: int,
        subscription_price: int,
        *,
        name: Optional[str] = None,
    ) -> ChatInviteLink:
        """Как bot.create_chat_subscription_invite_link(), но chat_id берётся из апдейта.
        
        Use this method to create a subscription invite link for a channel chat. The bot must have the can_invite_users administrator rights. The link can be edited using the method editChatSubscriptionInviteLink or revoked using the method revokeChatInviteLink. Returns the new invite link as a ChatInviteLink object.
        
        https://core.telegram.org/bots/api#createchatsubscriptioninvitelink
        
        Args:
            name: Invite link name; 0-32 characters
            subscription_period: The number of seconds the subscription will be active for before the next payment. Currently, it must always be 2592000 (30 days).
            subscription_price: The amount of Telegram Stars a user must pay initially and after each subsequent subscription period to be a member of the chat; 1-10000
        """
        return await self.bot.create_chat_subscription_invite_link(
            chat_id=self.chat_id,
            name=name,
            subscription_period=subscription_period,
            subscription_price=subscription_price,
        )

    async def edit_chat_subscription_invite_link(
        self,
        invite_link: str,
        *,
        name: Optional[str] = None,
    ) -> ChatInviteLink:
        """Как bot.edit_chat_subscription_invite_link(), но chat_id берётся из апдейта.
        
        Use this method to edit a subscription invite link created by the bot. The bot must have the can_invite_users administrator rights. Returns the edited invite link as a ChatInviteLink object.
        
        https://core.telegram.org/bots/api#editchatsubscriptioninvitelink
        
        Args:
            invite_link: The invite link to edit
            name: Invite link name; 0-32 characters
        """
        return await self.bot.edit_chat_subscription_invite_link(
            chat_id=self.chat_id,
            invite_link=invite_link,
            name=name,
        )

    async def revoke_chat_invite_link(
        self,
        invite_link: str,
    ) -> ChatInviteLink:
        """Как bot.revoke_chat_invite_link(), но chat_id берётся из апдейта.
        
        Use this method to revoke an invite link created by the bot. If the primary link is revoked, a new link is automatically generated. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Returns the revoked invite link as ChatInviteLink object.
        
        https://core.telegram.org/bots/api#revokechatinvitelink
        
        Args:
            invite_link: The invite link to revoke
        """
        return await self.bot.revoke_chat_invite_link(
            chat_id=self.chat_id,
            invite_link=invite_link,
        )

    async def approve_chat_join_request(
        self,
        user_id: int,
    ) -> bool:
        """Как bot.approve_chat_join_request(), но chat_id берётся из апдейта.
        
        Use this method to approve a chat join request. The bot must be an administrator in the chat for this to work and must have the can_invite_users administrator right. Returns True on success.
        
        https://core.telegram.org/bots/api#approvechatjoinrequest
        
        Args:
            user_id: Unique identifier of the target user
        """
        return await self.bot.approve_chat_join_request(
            chat_id=self.chat_id,
            user_id=user_id,
        )

    async def decline_chat_join_request(
        self,
        user_id: int,
    ) -> bool:
        """Как bot.decline_chat_join_request(), но chat_id берётся из апдейта.
        
        Use this method to decline a chat join request. The bot must be an administrator in the chat for this to work and must have the can_invite_users administrator right. Returns True on success.
        
        https://core.telegram.org/bots/api#declinechatjoinrequest
        
        Args:
            user_id: Unique identifier of the target user
        """
        return await self.bot.decline_chat_join_request(
            chat_id=self.chat_id,
            user_id=user_id,
        )

    async def set_chat_photo(
        self,
        photo: InputFile,
    ) -> bool:
        """Как bot.set_chat_photo(), но chat_id берётся из апдейта.
        
        Use this method to set a new profile photo for the chat. Photos can't be changed for private chats. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Returns True on success.
        
        https://core.telegram.org/bots/api#setchatphoto
        
        Args:
            photo: New chat photo, uploaded using multipart/form-data
        """
        return await self.bot.set_chat_photo(
            chat_id=self.chat_id,
            photo=photo,
        )

    async def delete_chat_photo(
        self,
    ) -> bool:
        """Как bot.delete_chat_photo(), но chat_id берётся из апдейта.
        
        Use this method to delete a chat photo. Photos can't be changed for private chats. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Returns True on success.
        
        https://core.telegram.org/bots/api#deletechatphoto
        """
        return await self.bot.delete_chat_photo(
            chat_id=self.chat_id,
        )

    async def set_chat_title(
        self,
        title: str,
    ) -> bool:
        """Как bot.set_chat_title(), но chat_id берётся из апдейта.
        
        Use this method to change the title of a chat. Titles can't be changed for private chats. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Returns True on success.
        
        https://core.telegram.org/bots/api#setchattitle
        
        Args:
            title: New chat title, 1-128 characters
        """
        return await self.bot.set_chat_title(
            chat_id=self.chat_id,
            title=title,
        )

    async def set_chat_description(
        self,
        *,
        description: Optional[str] = None,
    ) -> bool:
        """Как bot.set_chat_description(), но chat_id берётся из апдейта.
        
        Use this method to change the description of a group, a supergroup or a channel. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Returns True on success.
        
        https://core.telegram.org/bots/api#setchatdescription
        
        Args:
            description: New chat description, 0-255 characters
        """
        return await self.bot.set_chat_description(
            chat_id=self.chat_id,
            description=description,
        )

    async def pin_chat_message(
        self,
        *,
        business_connection_id: Optional[str] = None,
        message_id: Optional[int] = None,
        disable_notification: Optional[bool] = None,
    ) -> bool:
        """Как bot.pin_chat_message(), но chat_id берётся из апдейта.
        
        Use this method to add a message to the list of pinned messages in a chat. In private chats and channel direct messages chats, all non-service messages can be pinned. Conversely, the bot must be an administrator with the 'can_pin_messages' right or the 'can_edit_messages' right to pin messages in groups and channels respectively. Returns True on success.
        
        https://core.telegram.org/bots/api#pinchatmessage
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message will be pinned
            message_id: Identifier of a message to pin
            disable_notification: Pass True if it is not necessary to send a notification to all chat members about the new pinned message. Notifications are always disabled in channels and private chats.
        """
        return await self.bot.pin_chat_message(
            business_connection_id=business_connection_id,
            chat_id=self.chat_id,
            message_id=message_id if message_id is not None else self._require_message_id(),
            disable_notification=disable_notification,
        )

    async def unpin_chat_message(
        self,
        *,
        business_connection_id: Optional[str] = None,
        message_id: Optional[int] = None,
    ) -> bool:
        """Как bot.unpin_chat_message(), но chat_id берётся из апдейта.
        
        Use this method to remove a message from the list of pinned messages in a chat. In private chats and channel direct messages chats, all messages can be unpinned. Conversely, the bot must be an administrator with the 'can_pin_messages' right or the 'can_edit_messages' right to unpin messages in groups and channels respectively. Returns True on success.
        
        https://core.telegram.org/bots/api#unpinchatmessage
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message will be unpinned
            message_id: Identifier of the message to unpin. Required if business_connection_id is specified. If not specified, the most recent pinned message (by sending date) will be unpinned.
        """
        return await self.bot.unpin_chat_message(
            business_connection_id=business_connection_id,
            chat_id=self.chat_id,
            message_id=message_id,
        )

    async def unpin_all_chat_messages(
        self,
    ) -> bool:
        """Как bot.unpin_all_chat_messages(), но chat_id берётся из апдейта.
        
        Use this method to clear the list of pinned messages in a chat. In private chats and channel direct messages chats, no additional rights are required to unpin all pinned messages. Conversely, the bot must be an administrator with the 'can_pin_messages' right or the 'can_edit_messages' right to unpin all pinned messages in groups and channels respectively. Returns True on success.
        
        https://core.telegram.org/bots/api#unpinallchatmessages
        """
        return await self.bot.unpin_all_chat_messages(
            chat_id=self.chat_id,
        )

    async def leave_chat(
        self,
    ) -> bool:
        """Как bot.leave_chat(), но chat_id берётся из апдейта.
        
        Use this method for your bot to leave a group, supergroup or channel. Returns True on success.
        
        https://core.telegram.org/bots/api#leavechat
        """
        return await self.bot.leave_chat(
            chat_id=self.chat_id,
        )

    async def get_chat(
        self,
    ) -> ChatFullInfo:
        """Как bot.get_chat(), но chat_id берётся из апдейта.
        
        Use this method to get up-to-date information about the chat. Returns a ChatFullInfo object on success.
        
        https://core.telegram.org/bots/api#getchat
        """
        return await self.bot.get_chat(
            chat_id=self.chat_id,
        )

    async def get_chat_administrators(
        self,
        *,
        return_bots: Optional[bool] = None,
    ) -> List[ChatMember]:
        """Как bot.get_chat_administrators(), но chat_id берётся из апдейта.
        
        Use this method to get a list of administrators in a chat. Returns an Array of ChatMember objects.
        
        https://core.telegram.org/bots/api#getchatadministrators
        
        Args:
            return_bots: Pass True to additionally receive all bots that are administrators of the chat. By default, bots other than the current bot are omitted.
        """
        return await self.bot.get_chat_administrators(
            chat_id=self.chat_id,
            return_bots=return_bots,
        )

    async def get_chat_member_count(
        self,
    ) -> int:
        """Как bot.get_chat_member_count(), но chat_id берётся из апдейта.
        
        Use this method to get the number of members in a chat. Returns Integer on success.
        
        https://core.telegram.org/bots/api#getchatmembercount
        """
        return await self.bot.get_chat_member_count(
            chat_id=self.chat_id,
        )

    async def get_chat_member(
        self,
        user_id: int,
    ) -> ChatMember:
        """Как bot.get_chat_member(), но chat_id берётся из апдейта.
        
        Use this method to get information about a member of a chat. The method is only guaranteed to work for other users if the bot is an administrator in the chat. Returns a ChatMember object on success.
        
        https://core.telegram.org/bots/api#getchatmember
        
        Args:
            user_id: Unique identifier of the target user
        """
        return await self.bot.get_chat_member(
            chat_id=self.chat_id,
            user_id=user_id,
        )

    async def set_chat_sticker_set(
        self,
        sticker_set_name: str,
    ) -> bool:
        """Как bot.set_chat_sticker_set(), но chat_id берётся из апдейта.
        
        Use this method to set a new group sticker set for a supergroup. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Use the field can_set_sticker_set optionally returned in getChat requests to check if the bot can use this method. Returns True on success.
        
        https://core.telegram.org/bots/api#setchatstickerset
        
        Args:
            sticker_set_name: Name of the sticker set to be set as the group sticker set
        """
        return await self.bot.set_chat_sticker_set(
            chat_id=self.chat_id,
            sticker_set_name=sticker_set_name,
        )

    async def delete_chat_sticker_set(
        self,
    ) -> bool:
        """Как bot.delete_chat_sticker_set(), но chat_id берётся из апдейта.
        
        Use this method to delete a group sticker set from a supergroup. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Use the field can_set_sticker_set optionally returned in getChat requests to check if the bot can use this method. Returns True on success.
        
        https://core.telegram.org/bots/api#deletechatstickerset
        """
        return await self.bot.delete_chat_sticker_set(
            chat_id=self.chat_id,
        )

    async def create_forum_topic(
        self,
        name: str,
        *,
        icon_color: Optional[int] = None,
        icon_custom_emoji_id: Optional[str] = None,
    ) -> ForumTopic:
        """Как bot.create_forum_topic(), но chat_id берётся из апдейта.
        
        Use this method to create a topic in a forum supergroup chat or a private chat with a user. In the case of a supergroup chat the bot must be an administrator in the chat for this to work and must have the can_manage_topics administrator right. Returns information about the created topic as a ForumTopic object.
        
        https://core.telegram.org/bots/api#createforumtopic
        
        Args:
            name: Topic name, 1-128 characters
            icon_color: Color of the topic icon in RGB format. Currently, must be one of 7322096 (0x6FB9F0), 16766590 (0xFFD67E), 13338331 (0xCB86DB), 9367192 (0x8EEE98), 16749490 (0xFF93B2), or 16478047 (0xFB6F5F).
            icon_custom_emoji_id: Unique identifier of the custom emoji shown as the topic icon. Use getForumTopicIconStickers to get all allowed custom emoji identifiers.
        """
        return await self.bot.create_forum_topic(
            chat_id=self.chat_id,
            name=name,
            icon_color=icon_color,
            icon_custom_emoji_id=icon_custom_emoji_id,
        )

    async def edit_forum_topic(
        self,
        message_thread_id: int,
        *,
        name: Optional[str] = None,
        icon_custom_emoji_id: Optional[str] = None,
    ) -> bool:
        """Как bot.edit_forum_topic(), но chat_id берётся из апдейта.
        
        Use this method to edit name and icon of a topic in a forum supergroup chat or a private chat with a user. In the case of a supergroup chat the bot must be an administrator in the chat for this to work and must have the can_manage_topics administrator rights, unless it is the creator of the topic. Returns True on success.
        
        https://core.telegram.org/bots/api#editforumtopic
        
        Args:
            message_thread_id: Unique identifier for the target message thread of the forum topic
            name: New topic name, 0-128 characters. If not specified or empty, the current name of the topic will be kept.
            icon_custom_emoji_id: New unique identifier of the custom emoji shown as the topic icon. Use getForumTopicIconStickers to get all allowed custom emoji identifiers. Pass an empty string to remove the icon. If not specified, the current icon will be kept.
        """
        return await self.bot.edit_forum_topic(
            chat_id=self.chat_id,
            message_thread_id=message_thread_id,
            name=name,
            icon_custom_emoji_id=icon_custom_emoji_id,
        )

    async def close_forum_topic(
        self,
        message_thread_id: int,
    ) -> bool:
        """Как bot.close_forum_topic(), но chat_id берётся из апдейта.
        
        Use this method to close an open topic in a forum supergroup chat. The bot must be an administrator in the chat for this to work and must have the can_manage_topics administrator rights, unless it is the creator of the topic. Returns True on success.
        
        https://core.telegram.org/bots/api#closeforumtopic
        
        Args:
            message_thread_id: Unique identifier for the target message thread of the forum topic
        """
        return await self.bot.close_forum_topic(
            chat_id=self.chat_id,
            message_thread_id=message_thread_id,
        )

    async def reopen_forum_topic(
        self,
        message_thread_id: int,
    ) -> bool:
        """Как bot.reopen_forum_topic(), но chat_id берётся из апдейта.
        
        Use this method to reopen a closed topic in a forum supergroup chat. The bot must be an administrator in the chat for this to work and must have the can_manage_topics administrator rights, unless it is the creator of the topic. Returns True on success.
        
        https://core.telegram.org/bots/api#reopenforumtopic
        
        Args:
            message_thread_id: Unique identifier for the target message thread of the forum topic
        """
        return await self.bot.reopen_forum_topic(
            chat_id=self.chat_id,
            message_thread_id=message_thread_id,
        )

    async def delete_forum_topic(
        self,
        message_thread_id: int,
    ) -> bool:
        """Как bot.delete_forum_topic(), но chat_id берётся из апдейта.
        
        Use this method to delete a forum topic along with all its messages in a forum supergroup chat or a private chat with a user. In the case of a supergroup chat the bot must be an administrator in the chat for this to work and must have the can_delete_messages administrator rights. Returns True on success.
        
        https://core.telegram.org/bots/api#deleteforumtopic
        
        Args:
            message_thread_id: Unique identifier for the target message thread of the forum topic
        """
        return await self.bot.delete_forum_topic(
            chat_id=self.chat_id,
            message_thread_id=message_thread_id,
        )

    async def unpin_all_forum_topic_messages(
        self,
        message_thread_id: int,
    ) -> bool:
        """Как bot.unpin_all_forum_topic_messages(), но chat_id берётся из апдейта.
        
        Use this method to clear the list of pinned messages in a forum topic in a forum supergroup chat or a private chat with a user. In the case of a supergroup chat the bot must be an administrator in the chat for this to work and must have the can_pin_messages administrator right in the supergroup. Returns True on success.
        
        https://core.telegram.org/bots/api#unpinallforumtopicmessages
        
        Args:
            message_thread_id: Unique identifier for the target message thread of the forum topic
        """
        return await self.bot.unpin_all_forum_topic_messages(
            chat_id=self.chat_id,
            message_thread_id=message_thread_id,
        )

    async def edit_general_forum_topic(
        self,
        name: str,
    ) -> bool:
        """Как bot.edit_general_forum_topic(), но chat_id берётся из апдейта.
        
        Use this method to edit the name of the 'General' topic in a forum supergroup chat. The bot must be an administrator in the chat for this to work and must have the can_manage_topics administrator rights. Returns True on success.
        
        https://core.telegram.org/bots/api#editgeneralforumtopic
        
        Args:
            name: New topic name, 1-128 characters
        """
        return await self.bot.edit_general_forum_topic(
            chat_id=self.chat_id,
            name=name,
        )

    async def close_general_forum_topic(
        self,
    ) -> bool:
        """Как bot.close_general_forum_topic(), но chat_id берётся из апдейта.
        
        Use this method to close an open 'General' topic in a forum supergroup chat. The bot must be an administrator in the chat for this to work and must have the can_manage_topics administrator rights. Returns True on success.
        
        https://core.telegram.org/bots/api#closegeneralforumtopic
        """
        return await self.bot.close_general_forum_topic(
            chat_id=self.chat_id,
        )

    async def reopen_general_forum_topic(
        self,
    ) -> bool:
        """Как bot.reopen_general_forum_topic(), но chat_id берётся из апдейта.
        
        Use this method to reopen a closed 'General' topic in a forum supergroup chat. The bot must be an administrator in the chat for this to work and must have the can_manage_topics administrator rights. The topic will be automatically unhidden if it was hidden. Returns True on success.
        
        https://core.telegram.org/bots/api#reopengeneralforumtopic
        """
        return await self.bot.reopen_general_forum_topic(
            chat_id=self.chat_id,
        )

    async def hide_general_forum_topic(
        self,
    ) -> bool:
        """Как bot.hide_general_forum_topic(), но chat_id берётся из апдейта.
        
        Use this method to hide the 'General' topic in a forum supergroup chat. The bot must be an administrator in the chat for this to work and must have the can_manage_topics administrator rights. The topic will be automatically closed if it was open. Returns True on success.
        
        https://core.telegram.org/bots/api#hidegeneralforumtopic
        """
        return await self.bot.hide_general_forum_topic(
            chat_id=self.chat_id,
        )

    async def unhide_general_forum_topic(
        self,
    ) -> bool:
        """Как bot.unhide_general_forum_topic(), но chat_id берётся из апдейта.
        
        Use this method to unhide the 'General' topic in a forum supergroup chat. The bot must be an administrator in the chat for this to work and must have the can_manage_topics administrator rights. Returns True on success.
        
        https://core.telegram.org/bots/api#unhidegeneralforumtopic
        """
        return await self.bot.unhide_general_forum_topic(
            chat_id=self.chat_id,
        )

    async def unpin_all_general_forum_topic_messages(
        self,
    ) -> bool:
        """Как bot.unpin_all_general_forum_topic_messages(), но chat_id берётся из апдейта.
        
        Use this method to clear the list of pinned messages in a General forum topic. The bot must be an administrator in the chat for this to work and must have the can_pin_messages administrator right in the supergroup. Returns True on success.
        
        https://core.telegram.org/bots/api#unpinallgeneralforumtopicmessages
        """
        return await self.bot.unpin_all_general_forum_topic_messages(
            chat_id=self.chat_id,
        )

    async def answer_callback_query(
        self: ContextMethods[_TCallbackQuery],
        text: Optional[str] = None,
        *,
        show_alert: Optional[bool] = None,
        url: Optional[str] = None,
        cache_time: Optional[int] = None,
    ) -> bool:
        """Как bot.answer_callback_query(), но id запроса берётся из апдейта.
        
        Use this method to send answers to callback queries sent from inline keyboards. The answer will be displayed to the user as a notification at the top of the chat screen or as an alert. On success, True is returned.
        
        https://core.telegram.org/bots/api#answercallbackquery
        
        Args:
            text: Text of the notification. If not specified, nothing will be shown to the user, 0-200 characters.
            show_alert: If True, an alert will be shown by the client instead of a notification at the top of the chat screen. Defaults to False.
            url: URL that will be opened by the user's client. If you have created a Game and accepted the conditions via @BotFather, specify the URL that opens your game - note that this will only work if the query comes from a callback_game button. Otherwise, you may use links like t.me/your_bot?start=XXXX that open your bot with a parameter.
            cache_time: The maximum amount of time in seconds that the result of the callback query may be cached client-side. Defaults to 0.
        """
        return await self.bot.answer_callback_query(
            callback_query_id=self._event_id("callback_query"),
            text=text,
            show_alert=show_alert,
            url=url,
            cache_time=cache_time,
        )

    async def get_user_chat_boosts(
        self,
        user_id: int,
    ) -> UserChatBoosts:
        """Как bot.get_user_chat_boosts(), но chat_id берётся из апдейта.
        
        Use this method to get the list of boosts added to a chat by a user. Requires administrator rights in the chat. Returns a UserChatBoosts object.
        
        https://core.telegram.org/bots/api#getuserchatboosts
        
        Args:
            user_id: Unique identifier of the target user
        """
        return await self.bot.get_user_chat_boosts(
            chat_id=self.chat_id,
            user_id=user_id,
        )

    async def verify_chat(
        self,
        *,
        custom_description: Optional[str] = None,
    ) -> bool:
        """Как bot.verify_chat(), но chat_id берётся из апдейта.
        
        Verifies a chat on behalf of the organization which is represented by the bot. Returns True on success.
        
        https://core.telegram.org/bots/api#verifychat
        
        Args:
            custom_description: Custom description for the verification; 0-70 characters. Must be empty if the organization isn't allowed to provide a custom verification description.
        """
        return await self.bot.verify_chat(
            chat_id=self.chat_id,
            custom_description=custom_description,
        )

    async def remove_chat_verification(
        self,
    ) -> bool:
        """Как bot.remove_chat_verification(), но chat_id берётся из апдейта.
        
        Removes verification from a chat that is currently verified on behalf of the organization represented by the bot. Returns True on success.
        
        https://core.telegram.org/bots/api#removechatverification
        """
        return await self.bot.remove_chat_verification(
            chat_id=self.chat_id,
        )

    async def read_business_message(
        self,
        business_connection_id: str,
        *,
        message_id: Optional[int] = None,
    ) -> bool:
        """Как bot.read_business_message(), но chat_id берётся из апдейта.
        
        Marks incoming message as read on behalf of a business account. Requires the can_read_messages business bot right. Returns True on success.
        
        https://core.telegram.org/bots/api#readbusinessmessage
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which to read the message
            message_id: Unique identifier of the message to mark as read
        """
        return await self.bot.read_business_message(
            business_connection_id=business_connection_id,
            chat_id=self.chat_id,
            message_id=message_id if message_id is not None else self._require_message_id(),
        )

    async def get_chat_gifts(
        self,
        *,
        exclude_unsaved: Optional[bool] = None,
        exclude_saved: Optional[bool] = None,
        exclude_unlimited: Optional[bool] = None,
        exclude_limited_upgradable: Optional[bool] = None,
        exclude_limited_non_upgradable: Optional[bool] = None,
        exclude_from_blockchain: Optional[bool] = None,
        exclude_unique: Optional[bool] = None,
        sort_by_price: Optional[bool] = None,
        offset: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> OwnedGifts:
        """Как bot.get_chat_gifts(), но chat_id берётся из апдейта.
        
        Returns the gifts owned by a chat. Returns OwnedGifts on success.
        
        https://core.telegram.org/bots/api#getchatgifts
        
        Args:
            exclude_unsaved: Pass True to exclude gifts that aren't saved to the chat's profile page. Always True, unless the bot has the can_post_messages administrator right in the channel.
            exclude_saved: Pass True to exclude gifts that are saved to the chat's profile page. Always False, unless the bot has the can_post_messages administrator right in the channel.
            exclude_unlimited: Pass True to exclude gifts that can be purchased an unlimited number of times
            exclude_limited_upgradable: Pass True to exclude gifts that can be purchased a limited number of times and can be upgraded to unique
            exclude_limited_non_upgradable: Pass True to exclude gifts that can be purchased a limited number of times and can't be upgraded to unique
            exclude_from_blockchain: Pass True to exclude gifts that were assigned from the TON blockchain and can't be resold or transferred in Telegram
            exclude_unique: Pass True to exclude unique gifts
            sort_by_price: Pass True to sort results by gift price instead of send date. Sorting is applied before pagination.
            offset: Offset of the first entry to return as received from the previous request; use an empty string to get the first chunk of results
            limit: The maximum number of gifts to be returned; 1-100. Defaults to 100.
        """
        return await self.bot.get_chat_gifts(
            chat_id=self.chat_id,
            exclude_unsaved=exclude_unsaved,
            exclude_saved=exclude_saved,
            exclude_unlimited=exclude_unlimited,
            exclude_limited_upgradable=exclude_limited_upgradable,
            exclude_limited_non_upgradable=exclude_limited_non_upgradable,
            exclude_from_blockchain=exclude_from_blockchain,
            exclude_unique=exclude_unique,
            sort_by_price=sort_by_price,
            offset=offset,
            limit=limit,
        )

    async def edit_message_text(
        self,
        text: Optional[str] = None,
        *,
        business_connection_id: Optional[str] = None,
        chat_id: Optional[Union[int, str]] = None,
        message_id: Optional[int] = None,
        inline_message_id: Optional[str] = None,
        parse_mode: Optional[str] = None,
        entities: Optional[List[MessageEntity]] = None,
        link_preview_options: Optional[LinkPreviewOptions] = None,
        rich_message: Optional[InputRichMessage] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ) -> Union[Message, bool]:
        """Как bot.edit_message_text(), но правит сообщение апдейта (или inline-сообщение), если цель не задана.
        
        Use this method to edit text, rich and game messages. On success, if the edited message is not an inline message, the edited Message is returned, otherwise True is returned. Note that business messages that were not sent by the bot and do not contain an inline keyboard can only be edited within 48 hours from the time they were sent.
        
        https://core.telegram.org/bots/api#editmessagetext
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message to be edited was sent
            chat_id: Required if inline_message_id is not specified. Unique identifier for the target chat or username of the target bot, supergroup or channel in the format @username.
            message_id: Required if inline_message_id is not specified. Identifier of the message to edit.
            inline_message_id: Required if chat_id and message_id are not specified. Identifier of the inline message.
            text: New text of the message, 1-4096 characters after entity parsing; required if rich_message isn't specified
            parse_mode: Mode for parsing entities in the message text. See formatting options for more details.
            entities: A JSON-serialized list of special entities that appear in message text, which can be specified instead of parse_mode
            link_preview_options: Link preview generation options for the message
            rich_message: New rich content of the message; required if text isn't specified. Direct upload of new files and explicit upload of files by a URL isn't supported when an inline message is edited.
            reply_markup: A JSON-serialized object for an inline keyboard
        """
        chat_id, message_id, inline_message_id = self._message_target(chat_id, message_id, inline_message_id)
        return await self.bot.edit_message_text(
            business_connection_id=business_connection_id,
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
            text=text,
            parse_mode=parse_mode,
            entities=entities,
            link_preview_options=link_preview_options,
            rich_message=rich_message,
            reply_markup=reply_markup,
        )

    async def edit_message_caption(
        self,
        caption: Optional[str] = None,
        *,
        business_connection_id: Optional[str] = None,
        chat_id: Optional[Union[int, str]] = None,
        message_id: Optional[int] = None,
        inline_message_id: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        show_caption_above_media: Optional[bool] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ) -> Union[Message, bool]:
        """Как bot.edit_message_caption(), но правит сообщение апдейта (или inline-сообщение), если цель не задана.
        
        Use this method to edit captions of messages. On success, if the edited message is not an inline message, the edited Message is returned, otherwise True is returned. Note that business messages that were not sent by the bot and do not contain an inline keyboard can only be edited within 48 hours from the time they were sent.
        
        https://core.telegram.org/bots/api#editmessagecaption
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message to be edited was sent
            chat_id: Required if inline_message_id is not specified. Unique identifier for the target chat or username of the target bot, supergroup or channel in the format @username.
            message_id: Required if inline_message_id is not specified. Identifier of the message to edit.
            inline_message_id: Required if chat_id and message_id are not specified. Identifier of the inline message.
            caption: New caption of the message, 0-1024 characters after entities parsing
            parse_mode: Mode for parsing entities in the message caption. See formatting options for more details.
            caption_entities: A JSON-serialized list of special entities that appear in the caption, which can be specified instead of parse_mode
            show_caption_above_media: Pass True if the caption must be shown above the message media. Supported only for animation, photo and video messages.
            reply_markup: A JSON-serialized object for an inline keyboard
        """
        chat_id, message_id, inline_message_id = self._message_target(chat_id, message_id, inline_message_id)
        return await self.bot.edit_message_caption(
            business_connection_id=business_connection_id,
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            show_caption_above_media=show_caption_above_media,
            reply_markup=reply_markup,
        )

    async def edit_message_media(
        self,
        media: InputMedia,
        *,
        business_connection_id: Optional[str] = None,
        chat_id: Optional[Union[int, str]] = None,
        message_id: Optional[int] = None,
        inline_message_id: Optional[str] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ) -> Union[Message, bool]:
        """Как bot.edit_message_media(), но правит сообщение апдейта (или inline-сообщение), если цель не задана.
        
        Use this method to edit animation, audio, document, live photo, photo, or video messages, or to replace a text or a rich message with a media. If a message is part of a message album, then it can be edited only to an audio for audio albums, only to a document for document albums and to a photo, a live photo, or a video otherwise. When an inline message is edited, a new file can't be uploaded; use a previously uploaded file via its file_id or specify a URL. On success, if the edited message is not an inline message, the edited Message is returned, otherwise True is returned. Note that business messages that were not sent by the bot and do not contain an inline keyboard can only be edited within 48 hours from the time they were sent.
        
        https://core.telegram.org/bots/api#editmessagemedia
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message to be edited was sent
            chat_id: Required if inline_message_id is not specified. Unique identifier for the target chat or username of the target bot, supergroup or channel in the format @username.
            message_id: Required if inline_message_id is not specified. Identifier of the message to edit.
            inline_message_id: Required if chat_id and message_id are not specified. Identifier of the inline message.
            media: A JSON-serialized object for the new media content of the message
            reply_markup: A JSON-serialized object for a new inline keyboard
        """
        chat_id, message_id, inline_message_id = self._message_target(chat_id, message_id, inline_message_id)
        return await self.bot.edit_message_media(
            business_connection_id=business_connection_id,
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
            media=media,
            reply_markup=reply_markup,
        )

    async def edit_message_live_location(
        self,
        latitude: float,
        longitude: float,
        *,
        business_connection_id: Optional[str] = None,
        chat_id: Optional[Union[int, str]] = None,
        message_id: Optional[int] = None,
        inline_message_id: Optional[str] = None,
        live_period: Optional[int] = None,
        horizontal_accuracy: Optional[float] = None,
        heading: Optional[int] = None,
        proximity_alert_radius: Optional[int] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ) -> Union[Message, bool]:
        """Как bot.edit_message_live_location(), но правит сообщение апдейта (или inline-сообщение), если цель не задана.
        
        Use this method to edit live location messages. A location can be edited until its live_period expires or editing is explicitly disabled by a call to stopMessageLiveLocation. On success, if the edited message is not an inline message, the edited Message is returned, otherwise True is returned.
        
        https://core.telegram.org/bots/api#editmessagelivelocation
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message to be edited was sent
            chat_id: Required if inline_message_id is not specified. Unique identifier for the target chat or username of the target bot, supergroup or channel in the format @username.
            message_id: Required if inline_message_id is not specified. Identifier of the message to edit.
            inline_message_id: Required if chat_id and message_id are not specified. Identifier of the inline message.
            latitude: Latitude of new location
            longitude: Longitude of new location
            live_period: New period in seconds during which the location can be updated, starting from the message send date. If 0x7FFFFFFF is specified, then the location can be updated forever. Otherwise, the new value must not exceed the current live_period by more than a day, and the live location expiration date must remain within the next 90 days. If not specified, then live_period remains unchanged.
            horizontal_accuracy: The radius of uncertainty for the location, measured in meters; 0-1500
            heading: Direction in which the user is moving, in degrees. Must be between 1 and 360 if specified.
            proximity_alert_radius: The maximum distance for proximity alerts about approaching another chat member, in meters. Must be between 1 and 100000 if specified.
            reply_markup: A JSON-serialized object for a new inline keyboard
        """
        chat_id, message_id, inline_message_id = self._message_target(chat_id, message_id, inline_message_id)
        return await self.bot.edit_message_live_location(
            business_connection_id=business_connection_id,
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
            latitude=latitude,
            longitude=longitude,
            live_period=live_period,
            horizontal_accuracy=horizontal_accuracy,
            heading=heading,
            proximity_alert_radius=proximity_alert_radius,
            reply_markup=reply_markup,
        )

    async def stop_message_live_location(
        self,
        *,
        business_connection_id: Optional[str] = None,
        chat_id: Optional[Union[int, str]] = None,
        message_id: Optional[int] = None,
        inline_message_id: Optional[str] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ) -> Union[Message, bool]:
        """Как bot.stop_message_live_location(), но правит сообщение апдейта (или inline-сообщение), если цель не задана.
        
        Use this method to stop updating a live location message before live_period expires. On success, if the message is not an inline message, the edited Message is returned, otherwise True is returned.
        
        https://core.telegram.org/bots/api#stopmessagelivelocation
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message to be edited was sent
            chat_id: Required if inline_message_id is not specified. Unique identifier for the target chat or username of the target bot, supergroup or channel in the format @username.
            message_id: Required if inline_message_id is not specified. Identifier of the message with live location to stop.
            inline_message_id: Required if chat_id and message_id are not specified. Identifier of the inline message.
            reply_markup: A JSON-serialized object for a new inline keyboard
        """
        chat_id, message_id, inline_message_id = self._message_target(chat_id, message_id, inline_message_id)
        return await self.bot.stop_message_live_location(
            business_connection_id=business_connection_id,
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
            reply_markup=reply_markup,
        )

    async def edit_message_checklist(
        self,
        business_connection_id: str,
        checklist: InputChecklist,
        *,
        message_id: Optional[int] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ) -> Message:
        """Как bot.edit_message_checklist(), но chat_id берётся из апдейта.
        
        Use this method to edit a checklist on behalf of a connected business account. On success, the edited Message is returned.
        
        https://core.telegram.org/bots/api#editmessagechecklist
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
            message_id: Unique identifier for the target message
            checklist: A JSON-serialized object for the new checklist
            reply_markup: A JSON-serialized object for the new inline keyboard for the message
        """
        return await self.bot.edit_message_checklist(
            business_connection_id=business_connection_id,
            chat_id=self.chat_id,
            message_id=message_id if message_id is not None else self._require_message_id(),
            checklist=checklist,
            reply_markup=reply_markup,
        )

    async def edit_message_reply_markup(
        self,
        *,
        business_connection_id: Optional[str] = None,
        chat_id: Optional[Union[int, str]] = None,
        message_id: Optional[int] = None,
        inline_message_id: Optional[str] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ) -> Union[Message, bool]:
        """Как bot.edit_message_reply_markup(), но правит сообщение апдейта (или inline-сообщение), если цель не задана.
        
        Use this method to edit only the reply markup of messages. On success, if the edited message is not an inline message, the edited Message is returned, otherwise True is returned. Note that business messages that were not sent by the bot and do not contain an inline keyboard can only be edited within 48 hours from the time they were sent.
        
        https://core.telegram.org/bots/api#editmessagereplymarkup
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message to be edited was sent
            chat_id: Required if inline_message_id is not specified. Unique identifier for the target chat or username of the target bot, supergroup or channel in the format @username.
            message_id: Required if inline_message_id is not specified. Identifier of the message to edit.
            inline_message_id: Required if chat_id and message_id are not specified. Identifier of the inline message.
            reply_markup: A JSON-serialized object for an inline keyboard
        """
        chat_id, message_id, inline_message_id = self._message_target(chat_id, message_id, inline_message_id)
        return await self.bot.edit_message_reply_markup(
            business_connection_id=business_connection_id,
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
            reply_markup=reply_markup,
        )

    async def stop_poll(
        self,
        *,
        business_connection_id: Optional[str] = None,
        message_id: Optional[int] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ) -> Poll:
        """Как bot.stop_poll(), но chat_id берётся из апдейта.
        
        Use this method to stop a poll which was sent by the bot. On success, the stopped Poll is returned.
        
        https://core.telegram.org/bots/api#stoppoll
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message to be edited was sent
            message_id: Identifier of the original message with the poll
            reply_markup: A JSON-serialized object for a new message inline keyboard
        """
        return await self.bot.stop_poll(
            business_connection_id=business_connection_id,
            chat_id=self.chat_id,
            message_id=message_id if message_id is not None else self._require_message_id(),
            reply_markup=reply_markup,
        )

    async def edit_ephemeral_message_text(
        self,
        receiver_user_id: int,
        ephemeral_message_id: int,
        *,
        text: Optional[str] = None,
        parse_mode: Optional[str] = None,
        entities: Optional[List[MessageEntity]] = None,
        rich_message: Optional[InputRichMessage] = None,
        link_preview_options: Optional[LinkPreviewOptions] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ) -> bool:
        """Как bot.edit_ephemeral_message_text(), но chat_id берётся из апдейта.
        
        Use this method to edit an ephemeral text or rich message. Note that it is not guaranteed that the user will receive the message edit event, especially if they are offline. On success, True is returned.
        
        https://core.telegram.org/bots/api#editephemeralmessagetext
        
        Args:
            receiver_user_id: Identifier of the user who received the message
            ephemeral_message_id: Identifier of the ephemeral message to edit
            text: New text of the message, 1-4096 characters after entity parsing; required if rich_message isn't specified
            parse_mode: Mode for parsing entities in the message text. See formatting options for more details.
            entities: A JSON-serialized list of special entities that appear in message text, which can be specified instead of parse_mode
            rich_message: New rich content of the message; required if text isn't specified
            link_preview_options: Link preview generation options for the message
            reply_markup: A JSON-serialized object for an inline keyboard
        """
        return await self.bot.edit_ephemeral_message_text(
            chat_id=self.chat_id,
            receiver_user_id=receiver_user_id,
            ephemeral_message_id=ephemeral_message_id,
            text=text,
            parse_mode=parse_mode,
            entities=entities,
            rich_message=rich_message,
            link_preview_options=link_preview_options,
            reply_markup=reply_markup,
        )

    async def edit_ephemeral_message_media(
        self,
        receiver_user_id: int,
        ephemeral_message_id: int,
        media: InputMedia,
        *,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ) -> bool:
        """Как bot.edit_ephemeral_message_media(), но chat_id берётся из апдейта.
        
        Use this method to edit the media of an ephemeral message. Note that it is not guaranteed that the user will receive the message edit event, especially if they are offline. On success, True is returned.
        
        https://core.telegram.org/bots/api#editephemeralmessagemedia
        
        Args:
            receiver_user_id: Identifier of the user who received the message
            ephemeral_message_id: Identifier of the ephemeral message to edit
            media: A JSON-serialized object for the new media content of the message
            reply_markup: A JSON-serialized object for an inline keyboard
        """
        return await self.bot.edit_ephemeral_message_media(
            chat_id=self.chat_id,
            receiver_user_id=receiver_user_id,
            ephemeral_message_id=ephemeral_message_id,
            media=media,
            reply_markup=reply_markup,
        )

    async def edit_ephemeral_message_caption(
        self,
        receiver_user_id: int,
        ephemeral_message_id: int,
        *,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        show_caption_above_media: Optional[bool] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ) -> bool:
        """Как bot.edit_ephemeral_message_caption(), но chat_id берётся из апдейта.
        
        Use this method to edit the caption of an ephemeral message. Note that it is not guaranteed that the user will receive the message edit event, especially if they are offline. On success, True is returned.
        
        https://core.telegram.org/bots/api#editephemeralmessagecaption
        
        Args:
            receiver_user_id: Identifier of the user who received the message
            ephemeral_message_id: Identifier of the ephemeral message to edit
            caption: New caption of the message, 0-1024 characters after entities parsing
            parse_mode: Mode for parsing entities in the message caption. See formatting options for more details.
            caption_entities: A JSON-serialized list of special entities that appear in the caption, which can be specified instead of parse_mode
            show_caption_above_media: Pass True if the caption must be shown above the message media. Supported only for animation, photo and video messages.
            reply_markup: A JSON-serialized object for an inline keyboard
        """
        return await self.bot.edit_ephemeral_message_caption(
            chat_id=self.chat_id,
            receiver_user_id=receiver_user_id,
            ephemeral_message_id=ephemeral_message_id,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            show_caption_above_media=show_caption_above_media,
            reply_markup=reply_markup,
        )

    async def edit_ephemeral_message_reply_markup(
        self,
        receiver_user_id: int,
        ephemeral_message_id: int,
        *,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ) -> bool:
        """Как bot.edit_ephemeral_message_reply_markup(), но chat_id берётся из апдейта.
        
        Use this method to edit only the reply markup of an ephemeral message. Note that it is not guaranteed that the user will receive the message edit event, especially if they are offline. On success, True is returned.
        
        https://core.telegram.org/bots/api#editephemeralmessagereplymarkup
        
        Args:
            receiver_user_id: Identifier of the user who received the message
            ephemeral_message_id: Identifier of the ephemeral message to edit
            reply_markup: A JSON-serialized object for an inline keyboard
        """
        return await self.bot.edit_ephemeral_message_reply_markup(
            chat_id=self.chat_id,
            receiver_user_id=receiver_user_id,
            ephemeral_message_id=ephemeral_message_id,
            reply_markup=reply_markup,
        )

    async def approve_suggested_post(
        self,
        *,
        message_id: Optional[int] = None,
        send_date: Optional[int] = None,
    ) -> bool:
        """Как bot.approve_suggested_post(), но chat_id берётся из апдейта.
        
        Use this method to approve a suggested post in a direct messages chat. The bot must have the 'can_post_messages' administrator right in the corresponding channel chat. Returns True on success.
        
        https://core.telegram.org/bots/api#approvesuggestedpost
        
        Args:
            message_id: Identifier of a suggested post message to approve
            send_date: Point in time (Unix timestamp) when the post is expected to be published; omit if the date has already been specified when the suggested post was created. If specified, then the date must be not more than 2678400 seconds (30 days) in the future.
        """
        return await self.bot.approve_suggested_post(
            chat_id=self.chat_id,
            message_id=message_id if message_id is not None else self._require_message_id(),
            send_date=send_date,
        )

    async def decline_suggested_post(
        self,
        *,
        message_id: Optional[int] = None,
        comment: Optional[str] = None,
    ) -> bool:
        """Как bot.decline_suggested_post(), но chat_id берётся из апдейта.
        
        Use this method to decline a suggested post in a direct messages chat. The bot must have the 'can_manage_direct_messages' administrator right in the corresponding channel chat. Returns True on success.
        
        https://core.telegram.org/bots/api#declinesuggestedpost
        
        Args:
            message_id: Identifier of a suggested post message to decline
            comment: Comment for the creator of the suggested post; 0-128 characters
        """
        return await self.bot.decline_suggested_post(
            chat_id=self.chat_id,
            message_id=message_id if message_id is not None else self._require_message_id(),
            comment=comment,
        )

    async def delete_message(
        self,
        *,
        message_id: Optional[int] = None,
    ) -> bool:
        """Как bot.delete_message(), но chat_id берётся из апдейта.
        
        Use this method to delete a message, including service messages, with the following limitations:
        
        - A message can only be deleted if it was sent less than 48 hours ago.
        
        - Service messages about a supergroup, channel, or forum topic creation can't be deleted.
        
        - A dice message in a private chat can only be deleted if it was sent more than 24 hours ago.
        
        - Bots can delete outgoing messages in private chats, groups, and supergroups.
        
        - Bots can delete incoming messages in private chats.
        
        - Bots granted can_post_messages permissions can delete outgoing messages in channels.
        
        - If the bot is an administrator of a group, it can delete any message there.
        
        - If the bot has can_delete_messages administrator right in a supergroup or a channel, it can delete any message there.
        
        - If the bot has can_manage_direct_messages administrator right in a channel, it can delete any message in the corresponding direct messages chat.
        
        Returns True on success.
        
        https://core.telegram.org/bots/api#deletemessage
        
        Args:
            message_id: Identifier of the message to delete
        """
        return await self.bot.delete_message(
            chat_id=self.chat_id,
            message_id=message_id if message_id is not None else self._require_message_id(),
        )

    async def delete_messages(
        self,
        message_ids: List[int],
    ) -> bool:
        """Как bot.delete_messages(), но chat_id берётся из апдейта.
        
        Use this method to delete multiple messages simultaneously. If some of the specified messages can't be found, they are skipped. Returns True on success.
        
        https://core.telegram.org/bots/api#deletemessages
        
        Args:
            message_ids: A JSON-serialized list of 1-100 identifiers of messages to delete. See deleteMessage for limitations on which messages can be deleted.
        """
        return await self.bot.delete_messages(
            chat_id=self.chat_id,
            message_ids=message_ids,
        )

    async def delete_ephemeral_message(
        self,
        receiver_user_id: int,
        ephemeral_message_id: int,
    ) -> bool:
        """Как bot.delete_ephemeral_message(), но chat_id берётся из апдейта.
        
        Use this method to delete an ephemeral message. Note that it is not guaranteed that the user will receive the message deletion event, especially if they are offline. Returns True on success.
        
        https://core.telegram.org/bots/api#deleteephemeralmessage
        
        Args:
            receiver_user_id: Identifier of the user who received the message
            ephemeral_message_id: Identifier of the ephemeral message to delete
        """
        return await self.bot.delete_ephemeral_message(
            chat_id=self.chat_id,
            receiver_user_id=receiver_user_id,
            ephemeral_message_id=ephemeral_message_id,
        )

    async def delete_message_reaction(
        self,
        *,
        message_id: Optional[int] = None,
        user_id: Optional[int] = None,
        actor_chat_id: Optional[int] = None,
    ) -> bool:
        """Как bot.delete_message_reaction(), но chat_id берётся из апдейта.
        
        Use this method to remove a reaction from a message in a group or a supergroup chat. The bot must have the 'can_delete_messages' administrator right in the chat. Returns True on success.
        
        https://core.telegram.org/bots/api#deletemessagereaction
        
        Args:
            message_id: Identifier of the target message
            user_id: Identifier of the user whose reaction will be removed, if the reaction was added by a user
            actor_chat_id: Identifier of the chat whose reaction will be removed, if the reaction was added by a chat
        """
        return await self.bot.delete_message_reaction(
            chat_id=self.chat_id,
            message_id=message_id if message_id is not None else self._require_message_id(),
            user_id=user_id,
            actor_chat_id=actor_chat_id,
        )

    async def delete_all_message_reactions(
        self,
        *,
        user_id: Optional[int] = None,
        actor_chat_id: Optional[int] = None,
    ) -> bool:
        """Как bot.delete_all_message_reactions(), но chat_id берётся из апдейта.
        
        Use this method to remove up to 10000 recent reactions in a group or a supergroup chat added by a given user or chat. The bot must have the 'can_delete_messages' administrator right in the chat. Returns True on success.
        
        https://core.telegram.org/bots/api#deleteallmessagereactions
        
        Args:
            user_id: Identifier of the user whose reactions will be removed, if the reactions were added by a user
            actor_chat_id: Identifier of the chat whose reactions will be removed, if the reactions were added by a chat
        """
        return await self.bot.delete_all_message_reactions(
            chat_id=self.chat_id,
            user_id=user_id,
            actor_chat_id=actor_chat_id,
        )

    async def answer_sticker(
        self,
        sticker: Union[InputFile, str],
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        emoji: Optional[str] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_sticker(), но чат берётся из апдейта.
        
        Use this method to send static .WEBP, animated .TGS, or video .WEBM stickers. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendsticker
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
            message_thread_id: Unique identifier for the target message thread (topic) of a forum; for forum supergroups and private chats of bots with forum topic mode enabled only
            direct_messages_topic_id: Identifier of the direct messages topic to which the message will be sent; required if the message is sent to a direct messages chat
            ephemeral_message_parameters: A JSON-serialized object containing the parameters of the ephemeral message to send
            sticker: Sticker to send. Pass a file_id as String to send a file that exists on the Telegram servers (recommended), pass an HTTP URL as a String for Telegram to get a .WEBP sticker from the Internet, or upload a new .WEBP, .TGS, or .WEBM sticker using multipart/form-data. More information on Sending Files: https://core.telegram.org/bots/api#sending-files. Video and animated stickers can't be sent via an HTTP URL.
            emoji: Emoji associated with the sticker; only for just uploaded stickers
            disable_notification: Sends the message silently. Users will receive a notification with no sound.
            protect_content: Protects the contents of the sent message from forwarding and saving
            allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance.
            message_effect_id: Unique identifier of the message effect to be added to the message; for private chats only
            suggested_post_parameters: A JSON-serialized object containing the parameters of the suggested post to send; for direct messages chats only. If the message is sent as a reply to another suggested post, then that suggested post is automatically declined.
            reply_parameters: Description of the message to reply to
            reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user.
        """
        return await self.bot.send_sticker(
            business_connection_id=self._or_default("business_connection_id", business_connection_id),
            chat_id=self.chat_id,
            message_thread_id=self._or_default("message_thread_id", message_thread_id),
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            sticker=sticker,
            emoji=emoji,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def reply_sticker(
        self,
        sticker: Union[InputFile, str],
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        emoji: Optional[str] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_sticker(), но чат берётся из апдейта, сообщение цитирует сообщение апдейта.
        
        Use this method to send static .WEBP, animated .TGS, or video .WEBM stickers. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendsticker
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
            message_thread_id: Unique identifier for the target message thread (topic) of a forum; for forum supergroups and private chats of bots with forum topic mode enabled only
            direct_messages_topic_id: Identifier of the direct messages topic to which the message will be sent; required if the message is sent to a direct messages chat
            ephemeral_message_parameters: A JSON-serialized object containing the parameters of the ephemeral message to send
            sticker: Sticker to send. Pass a file_id as String to send a file that exists on the Telegram servers (recommended), pass an HTTP URL as a String for Telegram to get a .WEBP sticker from the Internet, or upload a new .WEBP, .TGS, or .WEBM sticker using multipart/form-data. More information on Sending Files: https://core.telegram.org/bots/api#sending-files. Video and animated stickers can't be sent via an HTTP URL.
            emoji: Emoji associated with the sticker; only for just uploaded stickers
            disable_notification: Sends the message silently. Users will receive a notification with no sound.
            protect_content: Protects the contents of the sent message from forwarding and saving
            allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance.
            message_effect_id: Unique identifier of the message effect to be added to the message; for private chats only
            suggested_post_parameters: A JSON-serialized object containing the parameters of the suggested post to send; for direct messages chats only. If the message is sent as a reply to another suggested post, then that suggested post is automatically declined.
            reply_parameters: Description of the message to reply to
            reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user.
        """
        return await self.bot.send_sticker(
            business_connection_id=self._or_default("business_connection_id", business_connection_id),
            chat_id=self.chat_id,
            message_thread_id=self._or_default("message_thread_id", message_thread_id),
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            sticker=sticker,
            emoji=emoji,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters if reply_parameters is not None else self._reply_parameters(),
            reply_markup=reply_markup,
        )

    async def answer_rich_message(
        self,
        rich_message: InputRichMessage,
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_rich_message(), но чат берётся из апдейта.
        
        Use this method to send rich messages. If the message contains a block with a media element, then the bot must have the right to send the media to the chat. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendrichmessage
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent. Bot can send rich messages on behalf of a business account only if the corresponding user can send rich messages.
            message_thread_id: Unique identifier for the target message thread (topic) of a forum; for forum supergroups and private chats of bots with forum topic mode enabled only
            direct_messages_topic_id: Identifier of the direct messages topic to which the message will be sent; required if the message is sent to a direct messages chat
            ephemeral_message_parameters: A JSON-serialized object containing the parameters of the ephemeral message to send
            rich_message: The message to be sent
            disable_notification: Sends the message silently. Users will receive a notification with no sound.
            protect_content: Protects the contents of the sent message from forwarding and saving
            allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance.
            message_effect_id: Unique identifier of the message effect to be added to the message; for private chats only
            suggested_post_parameters: A JSON-serialized object containing the parameters of the suggested post to send; for direct messages chats only. If the message is sent as a reply to another suggested post, then that suggested post is automatically declined.
            reply_parameters: Description of the message to reply to
            reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user.
        """
        return await self.bot.send_rich_message(
            business_connection_id=self._or_default("business_connection_id", business_connection_id),
            chat_id=self.chat_id,
            message_thread_id=self._or_default("message_thread_id", message_thread_id),
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            rich_message=rich_message,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def reply_rich_message(
        self,
        rich_message: InputRichMessage,
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        ephemeral_message_parameters: Optional[EphemeralMessageParameters] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None,
    ) -> Message:
        """Как bot.send_rich_message(), но чат берётся из апдейта, сообщение цитирует сообщение апдейта.
        
        Use this method to send rich messages. If the message contains a block with a media element, then the bot must have the right to send the media to the chat. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendrichmessage
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent. Bot can send rich messages on behalf of a business account only if the corresponding user can send rich messages.
            message_thread_id: Unique identifier for the target message thread (topic) of a forum; for forum supergroups and private chats of bots with forum topic mode enabled only
            direct_messages_topic_id: Identifier of the direct messages topic to which the message will be sent; required if the message is sent to a direct messages chat
            ephemeral_message_parameters: A JSON-serialized object containing the parameters of the ephemeral message to send
            rich_message: The message to be sent
            disable_notification: Sends the message silently. Users will receive a notification with no sound.
            protect_content: Protects the contents of the sent message from forwarding and saving
            allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance.
            message_effect_id: Unique identifier of the message effect to be added to the message; for private chats only
            suggested_post_parameters: A JSON-serialized object containing the parameters of the suggested post to send; for direct messages chats only. If the message is sent as a reply to another suggested post, then that suggested post is automatically declined.
            reply_parameters: Description of the message to reply to
            reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user.
        """
        return await self.bot.send_rich_message(
            business_connection_id=self._or_default("business_connection_id", business_connection_id),
            chat_id=self.chat_id,
            message_thread_id=self._or_default("message_thread_id", message_thread_id),
            direct_messages_topic_id=direct_messages_topic_id,
            ephemeral_message_parameters=ephemeral_message_parameters,
            rich_message=rich_message,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters if reply_parameters is not None else self._reply_parameters(),
            reply_markup=reply_markup,
        )

    async def answer_rich_message_draft(
        self,
        draft_id: int,
        rich_message: InputRichMessage,
        *,
        message_thread_id: Optional[int] = None,
        can_stop: Optional[bool] = None,
        keep_on_stop: Optional[bool] = None,
    ) -> bool:
        """Как bot.send_rich_message_draft(), но чат берётся из апдейта.
        
        Use this method to stream a partial rich message to a user while the message is being generated. Note that the streamed draft is ephemeral and acts as a temporary 30-second preview - once the output is finalized, you must call sendRichMessage with the complete message to persist it in the user's chat. Returns True on success.
        
        https://core.telegram.org/bots/api#sendrichmessagedraft
        
        Args:
            message_thread_id: Unique identifier for the target message thread
            draft_id: Unique identifier of the message draft; must be non-zero. Changes to drafts with the same identifier are animated. Otherwise, the draft is replaced without animation.
            rich_message: The partial message to be streamed. Direct upload of new files and explicit upload of files by a URL isn't supported.
            can_stop: Pass True to show the user a button to stop further drafts. The bot will receive an Update "stopped_message_generation" if the user presses the button.
            keep_on_stop: Pass True to keep the draft in the chat when the button is pressed. The draft will still disappear after a short time or if the bot sends a message. To fully preserve the partial draft, the bot should send it as a new message.
        """
        return await self.bot.send_rich_message_draft(
            chat_id=self.chat_id,
            message_thread_id=self._or_default("message_thread_id", message_thread_id),
            draft_id=draft_id,
            rich_message=rich_message,
            can_stop=can_stop,
            keep_on_stop=keep_on_stop,
        )

    async def answer_inline_query(
        self: ContextMethods[_TInlineQuery],
        results: List[InlineQueryResult],
        *,
        cache_time: Optional[int] = None,
        is_personal: Optional[bool] = None,
        next_offset: Optional[str] = None,
        button: Optional[InlineQueryResultsButton] = None,
    ) -> bool:
        """Как bot.answer_inline_query(), но id запроса берётся из апдейта.
        
        Use this method to send answers to an inline query. On success, True is returned.
        
        No more than 50 results per query are allowed.
        
        https://core.telegram.org/bots/api#answerinlinequery
        
        Args:
            results: A JSON-serialized Array of results for the inline query
            cache_time: The maximum amount of time in seconds that the result of the inline query may be cached on the server. Defaults to 300.
            is_personal: Pass True if results may be cached on the server side only for the user that sent the query. By default, results may be returned to any user who sends the same query.
            next_offset: Pass the offset that a client should send in the next query with the same text to receive more results. Pass an empty string if there are no more results or if you don't support pagination. Offset length can't exceed 64 bytes.
            button: A JSON-serialized object describing a button to be shown above inline query results
        """
        return await self.bot.answer_inline_query(
            inline_query_id=self._event_id("inline_query"),
            results=results,
            cache_time=cache_time,
            is_personal=is_personal,
            next_offset=next_offset,
            button=button,
        )

    async def answer_invoice(
        self,
        title: str,
        description: str,
        payload: str,
        currency: str,
        prices: List[LabeledPrice],
        *,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        provider_token: Optional[str] = None,
        max_tip_amount: Optional[int] = None,
        suggested_tip_amounts: Optional[List[int]] = None,
        start_parameter: Optional[str] = None,
        provider_data: Optional[str] = None,
        photo_url: Optional[str] = None,
        photo_size: Optional[int] = None,
        photo_width: Optional[int] = None,
        photo_height: Optional[int] = None,
        need_name: Optional[bool] = None,
        need_phone_number: Optional[bool] = None,
        need_email: Optional[bool] = None,
        need_shipping_address: Optional[bool] = None,
        send_phone_number_to_provider: Optional[bool] = None,
        send_email_to_provider: Optional[bool] = None,
        is_flexible: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ) -> Message:
        """Как bot.send_invoice(), но чат берётся из апдейта.
        
        Use this method to send invoices. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendinvoice
        
        Args:
            message_thread_id: Unique identifier for the target message thread (topic) of a forum; for forum supergroups and private chats of bots with forum topic mode enabled only
            direct_messages_topic_id: Identifier of the direct messages topic to which the message will be sent; required if the message is sent to a direct messages chat
            title: Product name, 1-32 characters
            description: Product description, 1-255 characters
            payload: Bot-defined invoice payload, 1-128 bytes. This will not be displayed to the user, use it for your internal processes.
            provider_token: Payment provider token, obtained via @BotFather. Pass an empty string for payments in Telegram Stars.
            currency: Three-letter ISO 4217 currency code, see more on currencies. Pass "XTR" for payments in Telegram Stars.
            prices: Price breakdown, a JSON-serialized list of components (e.g. product price, tax, discount, delivery cost, delivery tax, bonus, etc.). Must contain exactly one item for payments in Telegram Stars.
            max_tip_amount: The maximum accepted amount for tips in the smallest units of the currency (integer, not float/double). For example, for a maximum tip of US$ 1.45 pass max_tip_amount = 145. See the exp parameter in currencies.json, it shows the number of digits past the decimal point for each currency (2 for the majority of currencies). Defaults to 0. Not supported for payments in Telegram Stars.
            suggested_tip_amounts: A JSON-serialized Array of suggested amounts of tips in the smallest units of the currency (integer, not float/double). At most 4 suggested tip amounts can be specified. The suggested tip amounts must be positive, passed in a strictly increased order and must not exceed max_tip_amount.
            start_parameter: Unique deep-linking parameter. If left empty, forwarded copies of the sent message will have a Pay button, allowing multiple users to pay directly from the forwarded message, using the same invoice. If non-empty, forwarded copies of the sent message will have a URL button with a deep link to the bot (instead of a Pay button), with the value used as the start parameter.
            provider_data: JSON-serialized data about the invoice, which will be shared with the payment provider. A detailed description of required fields should be provided by the payment provider.
            photo_url: URL of the product photo for the invoice. Can be a photo of the goods or a marketing image for a service. People like it better when they see what they are paying for.
            photo_size: Photo size in bytes
            photo_width: Photo width
            photo_height: Photo height
            need_name: Pass True if you require the user's full name to complete the order. Ignored for payments in Telegram Stars.
            need_phone_number: Pass True if you require the user's phone number to complete the order. Ignored for payments in Telegram Stars.
            need_email: Pass True if you require the user's email address to complete the order. Ignored for payments in Telegram Stars.
            need_shipping_address: Pass True if you require the user's shipping address to complete the order. Ignored for payments in Telegram Stars.
            send_phone_number_to_provider: Pass True if the user's phone number should be sent to the provider. Ignored for payments in Telegram Stars.
            send_email_to_provider: Pass True if the user's email address should be sent to the provider. Ignored for payments in Telegram Stars.
            is_flexible: Pass True if the final price depends on the shipping method. Ignored for payments in Telegram Stars.
            disable_notification: Sends the message silently. Users will receive a notification with no sound.
            protect_content: Protects the contents of the sent message from forwarding and saving
            allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance.
            message_effect_id: Unique identifier of the message effect to be added to the message; for private chats only
            suggested_post_parameters: A JSON-serialized object containing the parameters of the suggested post to send; for direct messages chats only. If the message is sent as a reply to another suggested post, then that suggested post is automatically declined.
            reply_parameters: Description of the message to reply to
            reply_markup: A JSON-serialized object for an inline keyboard. If empty, one 'Pay total price' button will be shown. If not empty, the first button must be a Pay button.
        """
        return await self.bot.send_invoice(
            chat_id=self.chat_id,
            message_thread_id=self._or_default("message_thread_id", message_thread_id),
            direct_messages_topic_id=direct_messages_topic_id,
            title=title,
            description=description,
            payload=payload,
            provider_token=provider_token,
            currency=currency,
            prices=prices,
            max_tip_amount=max_tip_amount,
            suggested_tip_amounts=suggested_tip_amounts,
            start_parameter=start_parameter,
            provider_data=provider_data,
            photo_url=photo_url,
            photo_size=photo_size,
            photo_width=photo_width,
            photo_height=photo_height,
            need_name=need_name,
            need_phone_number=need_phone_number,
            need_email=need_email,
            need_shipping_address=need_shipping_address,
            send_phone_number_to_provider=send_phone_number_to_provider,
            send_email_to_provider=send_email_to_provider,
            is_flexible=is_flexible,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def reply_invoice(
        self,
        title: str,
        description: str,
        payload: str,
        currency: str,
        prices: List[LabeledPrice],
        *,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        provider_token: Optional[str] = None,
        max_tip_amount: Optional[int] = None,
        suggested_tip_amounts: Optional[List[int]] = None,
        start_parameter: Optional[str] = None,
        provider_data: Optional[str] = None,
        photo_url: Optional[str] = None,
        photo_size: Optional[int] = None,
        photo_width: Optional[int] = None,
        photo_height: Optional[int] = None,
        need_name: Optional[bool] = None,
        need_phone_number: Optional[bool] = None,
        need_email: Optional[bool] = None,
        need_shipping_address: Optional[bool] = None,
        send_phone_number_to_provider: Optional[bool] = None,
        send_email_to_provider: Optional[bool] = None,
        is_flexible: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ) -> Message:
        """Как bot.send_invoice(), но чат берётся из апдейта, сообщение цитирует сообщение апдейта.
        
        Use this method to send invoices. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendinvoice
        
        Args:
            message_thread_id: Unique identifier for the target message thread (topic) of a forum; for forum supergroups and private chats of bots with forum topic mode enabled only
            direct_messages_topic_id: Identifier of the direct messages topic to which the message will be sent; required if the message is sent to a direct messages chat
            title: Product name, 1-32 characters
            description: Product description, 1-255 characters
            payload: Bot-defined invoice payload, 1-128 bytes. This will not be displayed to the user, use it for your internal processes.
            provider_token: Payment provider token, obtained via @BotFather. Pass an empty string for payments in Telegram Stars.
            currency: Three-letter ISO 4217 currency code, see more on currencies. Pass "XTR" for payments in Telegram Stars.
            prices: Price breakdown, a JSON-serialized list of components (e.g. product price, tax, discount, delivery cost, delivery tax, bonus, etc.). Must contain exactly one item for payments in Telegram Stars.
            max_tip_amount: The maximum accepted amount for tips in the smallest units of the currency (integer, not float/double). For example, for a maximum tip of US$ 1.45 pass max_tip_amount = 145. See the exp parameter in currencies.json, it shows the number of digits past the decimal point for each currency (2 for the majority of currencies). Defaults to 0. Not supported for payments in Telegram Stars.
            suggested_tip_amounts: A JSON-serialized Array of suggested amounts of tips in the smallest units of the currency (integer, not float/double). At most 4 suggested tip amounts can be specified. The suggested tip amounts must be positive, passed in a strictly increased order and must not exceed max_tip_amount.
            start_parameter: Unique deep-linking parameter. If left empty, forwarded copies of the sent message will have a Pay button, allowing multiple users to pay directly from the forwarded message, using the same invoice. If non-empty, forwarded copies of the sent message will have a URL button with a deep link to the bot (instead of a Pay button), with the value used as the start parameter.
            provider_data: JSON-serialized data about the invoice, which will be shared with the payment provider. A detailed description of required fields should be provided by the payment provider.
            photo_url: URL of the product photo for the invoice. Can be a photo of the goods or a marketing image for a service. People like it better when they see what they are paying for.
            photo_size: Photo size in bytes
            photo_width: Photo width
            photo_height: Photo height
            need_name: Pass True if you require the user's full name to complete the order. Ignored for payments in Telegram Stars.
            need_phone_number: Pass True if you require the user's phone number to complete the order. Ignored for payments in Telegram Stars.
            need_email: Pass True if you require the user's email address to complete the order. Ignored for payments in Telegram Stars.
            need_shipping_address: Pass True if you require the user's shipping address to complete the order. Ignored for payments in Telegram Stars.
            send_phone_number_to_provider: Pass True if the user's phone number should be sent to the provider. Ignored for payments in Telegram Stars.
            send_email_to_provider: Pass True if the user's email address should be sent to the provider. Ignored for payments in Telegram Stars.
            is_flexible: Pass True if the final price depends on the shipping method. Ignored for payments in Telegram Stars.
            disable_notification: Sends the message silently. Users will receive a notification with no sound.
            protect_content: Protects the contents of the sent message from forwarding and saving
            allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance.
            message_effect_id: Unique identifier of the message effect to be added to the message; for private chats only
            suggested_post_parameters: A JSON-serialized object containing the parameters of the suggested post to send; for direct messages chats only. If the message is sent as a reply to another suggested post, then that suggested post is automatically declined.
            reply_parameters: Description of the message to reply to
            reply_markup: A JSON-serialized object for an inline keyboard. If empty, one 'Pay total price' button will be shown. If not empty, the first button must be a Pay button.
        """
        return await self.bot.send_invoice(
            chat_id=self.chat_id,
            message_thread_id=self._or_default("message_thread_id", message_thread_id),
            direct_messages_topic_id=direct_messages_topic_id,
            title=title,
            description=description,
            payload=payload,
            provider_token=provider_token,
            currency=currency,
            prices=prices,
            max_tip_amount=max_tip_amount,
            suggested_tip_amounts=suggested_tip_amounts,
            start_parameter=start_parameter,
            provider_data=provider_data,
            photo_url=photo_url,
            photo_size=photo_size,
            photo_width=photo_width,
            photo_height=photo_height,
            need_name=need_name,
            need_phone_number=need_phone_number,
            need_email=need_email,
            need_shipping_address=need_shipping_address,
            send_phone_number_to_provider=send_phone_number_to_provider,
            send_email_to_provider=send_email_to_provider,
            is_flexible=is_flexible,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters if reply_parameters is not None else self._reply_parameters(),
            reply_markup=reply_markup,
        )

    async def answer_shipping_query(
        self: ContextMethods[_TShippingQuery],
        ok: bool,
        *,
        shipping_options: Optional[List[ShippingOption]] = None,
        error_message: Optional[str] = None,
    ) -> bool:
        """Как bot.answer_shipping_query(), но id запроса берётся из апдейта.
        
        If you sent an invoice requesting a shipping address and the parameter is_flexible was specified, the Bot API will send an Update with a shipping_query field to the bot. Use this method to reply to shipping queries. On success, True is returned.
        
        https://core.telegram.org/bots/api#answershippingquery
        
        Args:
            ok: Pass True if delivery to the specified address is possible and False if there are any problems (for example, if delivery to the specified address is not possible)
            shipping_options: Required if ok is True. A JSON-serialized Array of available shipping options.
            error_message: Required if ok is False. Error message in human readable form that explains why it is impossible to complete the order (e.g. "Sorry, delivery to your desired address is unavailable"). Telegram will display this message to the user.
        """
        return await self.bot.answer_shipping_query(
            shipping_query_id=self._event_id("shipping_query"),
            ok=ok,
            shipping_options=shipping_options,
            error_message=error_message,
        )

    async def answer_pre_checkout_query(
        self: ContextMethods[_TPreCheckoutQuery],
        ok: bool,
        *,
        error_message: Optional[str] = None,
    ) -> bool:
        """Как bot.answer_pre_checkout_query(), но id запроса берётся из апдейта.
        
        Once the user has confirmed their payment and shipping details, the Bot API sends the final confirmation in the form of an Update with the field pre_checkout_query. Use this method to respond to such pre-checkout queries. On success, True is returned. Note: The Bot API must receive an answer within 10 seconds after the pre-checkout query was sent.
        
        https://core.telegram.org/bots/api#answerprecheckoutquery
        
        Args:
            ok: Specify True if everything is alright (goods are available, etc.) and the bot is ready to proceed with the order. Use False if there are any problems.
            error_message: Required if ok is False. Error message in human readable form that explains the reason for failure to proceed with the checkout (e.g. "Sorry, somebody just bought the last of our amazing black T-shirts while you were busy filling out your payment details. Please choose a different color or garment!"). Telegram will display this message to the user.
        """
        return await self.bot.answer_pre_checkout_query(
            pre_checkout_query_id=self._event_id("pre_checkout_query"),
            ok=ok,
            error_message=error_message,
        )

    async def answer_game(
        self,
        game_short_name: str,
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ) -> Message:
        """Как bot.send_game(), но чат берётся из апдейта.
        
        Use this method to send a game. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendgame
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
            message_thread_id: Unique identifier for the target message thread (topic) of a forum; for forum supergroups and private chats of bots with forum topic mode enabled only
            game_short_name: Short name of the game, serves as the unique identifier for the game. Set up your games via @BotFather.
            disable_notification: Sends the message silently. Users will receive a notification with no sound.
            protect_content: Protects the contents of the sent message from forwarding and saving
            allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance.
            message_effect_id: Unique identifier of the message effect to be added to the message; for private chats only
            reply_parameters: Description of the message to reply to
            reply_markup: A JSON-serialized object for an inline keyboard. If empty, one 'Play game_title' button will be shown. If not empty, the first button must launch the game.
        """
        return await self.bot.send_game(
            business_connection_id=self._or_default("business_connection_id", business_connection_id),
            chat_id=self.chat_id,
            message_thread_id=self._or_default("message_thread_id", message_thread_id),
            game_short_name=game_short_name,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def reply_game(
        self,
        game_short_name: str,
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ) -> Message:
        """Как bot.send_game(), но чат берётся из апдейта, сообщение цитирует сообщение апдейта.
        
        Use this method to send a game. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendgame
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
            message_thread_id: Unique identifier for the target message thread (topic) of a forum; for forum supergroups and private chats of bots with forum topic mode enabled only
            game_short_name: Short name of the game, serves as the unique identifier for the game. Set up your games via @BotFather.
            disable_notification: Sends the message silently. Users will receive a notification with no sound.
            protect_content: Protects the contents of the sent message from forwarding and saving
            allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance.
            message_effect_id: Unique identifier of the message effect to be added to the message; for private chats only
            reply_parameters: Description of the message to reply to
            reply_markup: A JSON-serialized object for an inline keyboard. If empty, one 'Play game_title' button will be shown. If not empty, the first button must launch the game.
        """
        return await self.bot.send_game(
            business_connection_id=self._or_default("business_connection_id", business_connection_id),
            chat_id=self.chat_id,
            message_thread_id=self._or_default("message_thread_id", message_thread_id),
            game_short_name=game_short_name,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters if reply_parameters is not None else self._reply_parameters(),
            reply_markup=reply_markup,
        )

    async def set_game_score(
        self,
        user_id: int,
        score: int,
        *,
        force: Optional[bool] = None,
        disable_edit_message: Optional[bool] = None,
        chat_id: Optional[int] = None,
        message_id: Optional[int] = None,
        inline_message_id: Optional[str] = None,
    ) -> Union[Message, bool]:
        """Как bot.set_game_score(), но правит сообщение апдейта (или inline-сообщение), если цель не задана.
        
        Use this method to set the score of the specified user in a game message. On success, if the message is not an inline message, the Message is returned, otherwise True is returned. Returns an error, if the new score is not greater than the user's current score in the chat and force is False.
        
        https://core.telegram.org/bots/api#setgamescore
        
        Args:
            user_id: User identifier
            score: New score, must be non-negative
            force: Pass True if the high score is allowed to decrease. This can be useful when fixing mistakes or banning cheaters.
            disable_edit_message: Pass True if the game message should not be automatically edited to include the current scoreboard
            chat_id: Required if inline_message_id is not specified. Unique identifier for the target chat.
            message_id: Required if inline_message_id is not specified. Identifier of the sent message.
            inline_message_id: Required if chat_id and message_id are not specified. Identifier of the inline message.
        """
        chat_id, message_id, inline_message_id = self._message_target(chat_id, message_id, inline_message_id)
        return await self.bot.set_game_score(
            user_id=user_id,
            score=score,
            force=force,
            disable_edit_message=disable_edit_message,
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
        )

    async def get_game_high_scores(
        self,
        user_id: int,
        *,
        chat_id: Optional[int] = None,
        message_id: Optional[int] = None,
        inline_message_id: Optional[str] = None,
    ) -> List[GameHighScore]:
        """Как bot.get_game_high_scores(), но правит сообщение апдейта (или inline-сообщение), если цель не задана.
        
        Use this method to get data for high score tables. Will return the score of the specified user and several of their neighbors in a game. Returns an Array of GameHighScore objects.
        
        https://core.telegram.org/bots/api#getgamehighscores
        
        Args:
            user_id: Target user id
            chat_id: Required if inline_message_id is not specified. Unique identifier for the target chat.
            message_id: Required if inline_message_id is not specified. Identifier of the sent message.
            inline_message_id: Required if chat_id and message_id are not specified. Identifier of the inline message.
        """
        chat_id, message_id, inline_message_id = self._message_target(chat_id, message_id, inline_message_id)
        return await self.bot.get_game_high_scores(
            user_id=user_id,
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
        )
