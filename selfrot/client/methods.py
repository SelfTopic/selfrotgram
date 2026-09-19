# АВТОГЕНЕРАЦИЯ: scripts/generate_types.py, Telegram Bot API 10.3, August 24, 2026.
# Руками не править — обновилась спека, перегенерировать.
# ruff: noqa
from __future__ import annotations

from typing import List, Optional, TypeVar, Union

from ..methods import *
from ..methods.base import TelegramMethod
from ..types import *

T = TypeVar("T")


class BotMethods:
    """Все методы Bot API. Не хватает только call(): его даёт Bot."""

    async def call(self, method: TelegramMethod[T]) -> T:
        raise NotImplementedError

    async def get_updates(
        self,
        *,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        timeout: Optional[int] = None,
        allowed_updates: Optional[List[str]] = None,
    ) -> List[Update]:
        """Use this method to receive incoming updates using long polling (wiki). Returns an Array of Update objects.
        
        https://core.telegram.org/bots/api#getupdates
        
        Args:
            offset: Identifier of the first update to be returned. Must be greater by one than the highest among the identifiers of previously received updates. By default, updates starting with the earliest unconfirmed update are returned. An update is considered confirmed as soon as getUpdates is called with an offset higher than its update_id. The negative offset can be specified to retrieve updates starting from -offset update from the end of the updates queue. All previous updates will be forgotten.
            limit: Limits the number of updates to be retrieved. Values between 1-100 are accepted. Defaults to 100.
            timeout: Timeout in seconds for long polling. Defaults to 0, i.e. usual short polling. Should be positive, short polling should be used for testing purposes only.
            allowed_updates: A JSON-serialized list of the update types you want your bot to receive. For example, specify ["message", "edited_channel_post", "callback_query"] to only receive updates of these types. See Update for a complete list of available update types. Specify an empty list to receive all update types except chat_member, message_reaction, and message_reaction_count (default). If not specified, the previous setting will be used. Please note that this parameter doesn't affect updates created before the call to getUpdates, so unwanted updates may be received for a short period of time.
        """
        return await self.call(GetUpdates(
            offset=offset,
            limit=limit,
            timeout=timeout,
            allowed_updates=allowed_updates,
        ))

    async def set_webhook(
        self,
        url: str,
        *,
        certificate: Optional[InputFile] = None,
        ip_address: Optional[str] = None,
        max_connections: Optional[int] = None,
        allowed_updates: Optional[List[str]] = None,
        drop_pending_updates: Optional[bool] = None,
        secret_token: Optional[str] = None,
    ) -> bool:
        """Use this method to specify a URL and receive incoming updates via an outgoing webhook. Whenever there is an update for the bot, we will send an HTTPS POST request to the specified URL, containing a JSON-serialized Update. In case of an unsuccessful request (a request with response HTTP status code different from 2XY), we will repeat the request and give up after a reasonable amount of attempts. Returns True on success.
        
        If you'd like to make sure that the webhook was set by you, you can specify secret data in the parameter secret_token. If specified, the request will contain a header "X-Telegram-Bot-Api-Secret-Token" with the secret token as content.
        
        https://core.telegram.org/bots/api#setwebhook
        
        Args:
            url: HTTPS URL to send updates to. Use an empty string to remove webhook integration.
            certificate: Upload your public key certificate so that the root certificate in use can be checked. See our self-signed guide for details.
            ip_address: The fixed IP address which will be used to send webhook requests instead of the IP address resolved through DNS
            max_connections: The maximum allowed number of simultaneous HTTPS connections to the webhook for update delivery, 1-100. Defaults to 40. Use lower values to limit the load on your bot's server, and higher values to increase your bot's throughput.
            allowed_updates: A JSON-serialized list of the update types you want your bot to receive. For example, specify ["message", "edited_channel_post", "callback_query"] to only receive updates of these types. See Update for a complete list of available update types. Specify an empty list to receive all update types except chat_member, message_reaction, and message_reaction_count (default). If not specified, the previous setting will be used. Please note that this parameter doesn't affect updates created before the call to the setWebhook, so unwanted updates may be received for a short period of time.
            drop_pending_updates: Pass True to drop all pending updates
            secret_token: A secret token to be sent in a header "X-Telegram-Bot-Api-Secret-Token" in every webhook request, 1-256 characters. Only characters A-Z, a-z, 0-9, _ and - are allowed. The header is useful to ensure that the request comes from a webhook set by you.
        """
        return await self.call(SetWebhook(
            url=url,
            certificate=certificate,
            ip_address=ip_address,
            max_connections=max_connections,
            allowed_updates=allowed_updates,
            drop_pending_updates=drop_pending_updates,
            secret_token=secret_token,
        ))

    async def delete_webhook(
        self,
        *,
        drop_pending_updates: Optional[bool] = None,
    ) -> bool:
        """Use this method to remove webhook integration if you decide to switch back to getUpdates. Returns True on success.
        
        https://core.telegram.org/bots/api#deletewebhook
        
        Args:
            drop_pending_updates: Pass True to drop all pending updates
        """
        return await self.call(DeleteWebhook(
            drop_pending_updates=drop_pending_updates,
        ))

    async def get_webhook_info(
        self,
    ) -> WebhookInfo:
        """Use this method to get current webhook status. Requires no parameters. On success, returns a WebhookInfo object. If the bot is using getUpdates, will return an object with the url field empty.
        
        https://core.telegram.org/bots/api#getwebhookinfo
        """
        return await self.call(GetWebhookInfo(
        ))

    async def get_me(
        self,
    ) -> User:
        """A simple method for testing your bot's authentication token. Requires no parameters. Returns basic information about the bot in form of a User object.
        
        https://core.telegram.org/bots/api#getme
        """
        return await self.call(GetMe(
        ))

    async def log_out(
        self,
    ) -> bool:
        """Use this method to log out from the cloud Bot API server before launching the bot locally. You must log out the bot before running it locally, otherwise there is no guarantee that the bot will receive updates. After a successful call, you can immediately log in on a local server, but will not be able to log in back to the cloud Bot API server for 10 minutes. Returns True on success. Requires no parameters.
        
        https://core.telegram.org/bots/api#logout
        """
        return await self.call(LogOut(
        ))

    async def close(
        self,
    ) -> bool:
        """Use this method to close the bot instance before moving it from one local server to another. You need to delete the webhook before calling this method to ensure that the bot isn't launched again after server restart. The method will return error 429 in the first 10 minutes after the bot is launched. Returns True on success. Requires no parameters.
        
        https://core.telegram.org/bots/api#close
        """
        return await self.call(Close(
        ))

    async def send_message(
        self,
        chat_id: Union[int, str],
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
        """Use this method to send text messages. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendmessage
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
            chat_id: Unique identifier for the target chat or username of the target bot, supergroup or channel in the format @username
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
        return await self.call(SendMessage(
            business_connection_id=business_connection_id,
            chat_id=chat_id,
            message_thread_id=message_thread_id,
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
        ))

    async def forward_message(
        self,
        chat_id: Union[int, str],
        from_chat_id: Union[int, str],
        message_id: int,
        *,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        video_start_timestamp: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
    ) -> Message:
        """Use this method to forward messages of any kind. Service messages and messages with protected content can't be forwarded. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#forwardmessage
        
        Args:
            chat_id: Unique identifier for the target chat or username of the target bot, supergroup or channel in the format @username
            message_thread_id: Unique identifier for the target message thread (topic) of a forum; for forum supergroups and private chats of bots with forum topic mode enabled only
            direct_messages_topic_id: Identifier of the direct messages topic to which the message will be forwarded; required if the message is forwarded to a direct messages chat
            from_chat_id: Unique identifier for the chat where the original message was sent (or username of the target bot, supergroup or channel in the format @username)
            video_start_timestamp: New start timestamp for the forwarded video in the message
            disable_notification: Sends the message silently. Users will receive a notification with no sound.
            protect_content: Protects the contents of the forwarded message from forwarding and saving
            message_effect_id: Unique identifier of the message effect to be added to the message; only available when forwarding to private chats
            suggested_post_parameters: A JSON-serialized object containing the parameters of the suggested post to send; for direct messages chats only
            message_id: Message identifier in the chat specified in from_chat_id
        """
        return await self.call(ForwardMessage(
            chat_id=chat_id,
            message_thread_id=message_thread_id,
            direct_messages_topic_id=direct_messages_topic_id,
            from_chat_id=from_chat_id,
            video_start_timestamp=video_start_timestamp,
            disable_notification=disable_notification,
            protect_content=protect_content,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            message_id=message_id,
        ))

    async def forward_messages(
        self,
        chat_id: Union[int, str],
        from_chat_id: Union[int, str],
        message_ids: List[int],
        *,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
    ) -> List[MessageId]:
        """Use this method to forward multiple messages of any kind. If some of the specified messages can't be found or forwarded, they are skipped. Service messages and messages with protected content can't be forwarded. Album grouping is kept for forwarded messages. On success, an Array of MessageId of the sent messages is returned.
        
        https://core.telegram.org/bots/api#forwardmessages
        
        Args:
            chat_id: Unique identifier for the target chat or username of the target bot, supergroup or channel in the format @username
            message_thread_id: Unique identifier for the target message thread (topic) of a forum; for forum supergroups and private chats of bots with forum topic mode enabled only
            direct_messages_topic_id: Identifier of the direct messages topic to which the messages will be forwarded; required if the messages are forwarded to a direct messages chat
            from_chat_id: Unique identifier for the chat where the original messages were sent (or username of the target bot, supergroup or channel in the format @username)
            message_ids: A JSON-serialized list of 1-100 identifiers of messages in the chat from_chat_id to forward. The identifiers must be specified in a strictly increasing order.
            disable_notification: Sends the messages silently. Users will receive a notification with no sound.
            protect_content: Protects the contents of the forwarded messages from forwarding and saving
        """
        return await self.call(ForwardMessages(
            chat_id=chat_id,
            message_thread_id=message_thread_id,
            direct_messages_topic_id=direct_messages_topic_id,
            from_chat_id=from_chat_id,
            message_ids=message_ids,
            disable_notification=disable_notification,
            protect_content=protect_content,
        ))

    async def copy_message(
        self,
        chat_id: Union[int, str],
        from_chat_id: Union[int, str],
        message_id: int,
        *,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
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
        """Use this method to copy messages of any kind. Service messages, paid media messages, giveaway messages, giveaway winners messages, and invoice messages can't be copied. A quiz poll can be copied only if the value of the field correct_option_ids is known to the bot. The method is analogous to the method forwardMessage, but the copied message doesn't have a link to the original message. Returns the MessageId of the sent message on success.
        
        https://core.telegram.org/bots/api#copymessage
        
        Args:
            chat_id: Unique identifier for the target chat or username of the target bot, supergroup or channel in the format @username
            message_thread_id: Unique identifier for the target message thread (topic) of a forum; for forum supergroups and private chats of bots with forum topic mode enabled only
            direct_messages_topic_id: Identifier of the direct messages topic to which the message will be sent; required if the message is sent to a direct messages chat
            from_chat_id: Unique identifier for the chat where the original message was sent (or username of the target bot, supergroup or channel in the format @username)
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
        return await self.call(CopyMessage(
            chat_id=chat_id,
            message_thread_id=message_thread_id,
            direct_messages_topic_id=direct_messages_topic_id,
            from_chat_id=from_chat_id,
            message_id=message_id,
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
        ))

    async def copy_messages(
        self,
        chat_id: Union[int, str],
        from_chat_id: Union[int, str],
        message_ids: List[int],
        *,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        remove_caption: Optional[bool] = None,
    ) -> List[MessageId]:
        """Use this method to copy messages of any kind. If some of the specified messages can't be found or copied, they are skipped. Service messages, paid media messages, giveaway messages, giveaway winners messages, and invoice messages can't be copied. A quiz poll can be copied only if the value of the field correct_option_ids is known to the bot. The method is analogous to the method forwardMessages, but the copied messages don't have a link to the original message. Album grouping is kept for copied messages. On success, an Array of MessageId of the sent messages is returned.
        
        https://core.telegram.org/bots/api#copymessages
        
        Args:
            chat_id: Unique identifier for the target chat or username of the target bot, supergroup or channel in the format @username
            message_thread_id: Unique identifier for the target message thread (topic) of a forum; for forum supergroups and private chats of bots with forum topic mode enabled only
            direct_messages_topic_id: Identifier of the direct messages topic to which the messages will be sent; required if the messages are sent to a direct messages chat
            from_chat_id: Unique identifier for the chat where the original messages were sent (or username of the target bot, supergroup or channel in the format @username)
            message_ids: A JSON-serialized list of 1-100 identifiers of messages in the chat from_chat_id to copy. The identifiers must be specified in a strictly increasing order.
            disable_notification: Sends the messages silently. Users will receive a notification with no sound.
            protect_content: Protects the contents of the sent messages from forwarding and saving
            remove_caption: Pass True to copy the messages without their captions
        """
        return await self.call(CopyMessages(
            chat_id=chat_id,
            message_thread_id=message_thread_id,
            direct_messages_topic_id=direct_messages_topic_id,
            from_chat_id=from_chat_id,
            message_ids=message_ids,
            disable_notification=disable_notification,
            protect_content=protect_content,
            remove_caption=remove_caption,
        ))

    async def send_photo(
        self,
        chat_id: Union[int, str],
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
        """Use this method to send photos. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendphoto
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
            chat_id: Unique identifier for the target chat or username of the target bot, supergroup or channel in the format @username
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
        return await self.call(SendPhoto(
            business_connection_id=business_connection_id,
            chat_id=chat_id,
            message_thread_id=message_thread_id,
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
        ))

    async def send_live_photo(
        self,
        chat_id: Union[int, str],
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
        """Use this method to send live photos. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendlivephoto
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
            chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
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
        return await self.call(SendLivePhoto(
            business_connection_id=business_connection_id,
            chat_id=chat_id,
            message_thread_id=message_thread_id,
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
        ))

    async def send_audio(
        self,
        chat_id: Union[int, str],
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
        """Use this method to send audio files, if you want Telegram clients to display them in the music player. Your audio must be in the .MP3 or .M4A format. On success, the sent Message is returned. Bots can currently send audio files of up to 50 MB in size, this limit may be changed in the future.
        
        For sending voice messages, use the sendVoice method instead.
        
        https://core.telegram.org/bots/api#sendaudio
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
            chat_id: Unique identifier for the target chat or username of the target bot, supergroup or channel in the format @username
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
        return await self.call(SendAudio(
            business_connection_id=business_connection_id,
            chat_id=chat_id,
            message_thread_id=message_thread_id,
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
        ))

    async def send_document(
        self,
        chat_id: Union[int, str],
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
        """Use this method to send general files. On success, the sent Message is returned. Bots can currently send files of any type of up to 50 MB in size, this limit may be changed in the future.
        
        https://core.telegram.org/bots/api#senddocument
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
            chat_id: Unique identifier for the target chat or username of the target bot, supergroup or channel in the format @username
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
        return await self.call(SendDocument(
            business_connection_id=business_connection_id,
            chat_id=chat_id,
            message_thread_id=message_thread_id,
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
        ))

    async def send_video(
        self,
        chat_id: Union[int, str],
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
        """Use this method to send video files, Telegram clients support MPEG4 videos (other formats may be sent as Document). On success, the sent Message is returned. Bots can currently send video files of up to 50 MB in size, this limit may be changed in the future.
        
        https://core.telegram.org/bots/api#sendvideo
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
            chat_id: Unique identifier for the target chat or username of the target bot, supergroup or channel in the format @username
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
        return await self.call(SendVideo(
            business_connection_id=business_connection_id,
            chat_id=chat_id,
            message_thread_id=message_thread_id,
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
        ))

    async def send_animation(
        self,
        chat_id: Union[int, str],
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
        """Use this method to send animation files (GIF or H.264/MPEG-4 AVC video without sound). On success, the sent Message is returned. Bots can currently send animation files of up to 50 MB in size, this limit may be changed in the future.
        
        https://core.telegram.org/bots/api#sendanimation
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
            chat_id: Unique identifier for the target chat or username of the target bot, supergroup or channel in the format @username
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
        return await self.call(SendAnimation(
            business_connection_id=business_connection_id,
            chat_id=chat_id,
            message_thread_id=message_thread_id,
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
        ))

    async def send_voice(
        self,
        chat_id: Union[int, str],
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
        """Use this method to send audio files, if you want Telegram clients to display the file as a playable voice message. For this to work, your audio must be in an .OGG file encoded with OPUS, or in .MP3 format, or in .M4A format (other formats may be sent as Audio or Document). On success, the sent Message is returned. Bots can currently send voice messages of up to 50 MB in size, this limit may be changed in the future.
        
        https://core.telegram.org/bots/api#sendvoice
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
            chat_id: Unique identifier for the target chat or username of the target bot, supergroup or channel in the format @username
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
        return await self.call(SendVoice(
            business_connection_id=business_connection_id,
            chat_id=chat_id,
            message_thread_id=message_thread_id,
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
        ))

    async def send_video_note(
        self,
        chat_id: Union[int, str],
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
        """Use this method to send a rounded square MPEG4 video of up to 1 minute long. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendvideonote
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
            chat_id: Unique identifier for the target chat or username of the target bot, supergroup or channel in the format @username
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
        return await self.call(SendVideoNote(
            business_connection_id=business_connection_id,
            chat_id=chat_id,
            message_thread_id=message_thread_id,
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
        ))

    async def send_paid_media(
        self,
        chat_id: Union[int, str],
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
        """Use this method to send paid media. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendpaidmedia
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
            chat_id: Unique identifier for the target chat or username of the target bot, supergroup or channel in the format @username. If the chat is a channel, all Telegram Star proceeds from this media will be credited to the chat's balance. Otherwise, they will be credited to the bot's balance.
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
        return await self.call(SendPaidMedia(
            business_connection_id=business_connection_id,
            chat_id=chat_id,
            message_thread_id=message_thread_id,
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
        ))

    async def send_media_group(
        self,
        chat_id: Union[int, str],
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
        """Use this method to send a group of photos, live photos, videos, documents or audios as an album. Documents and audio files can be only grouped in an album with messages of the same type. On success, an Array of Message objects that were sent is returned.
        
        https://core.telegram.org/bots/api#sendmediagroup
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
            chat_id: Unique identifier for the target chat or username of the target bot, supergroup or channel in the format @username
            message_thread_id: Unique identifier for the target message thread (topic) of a forum; for forum supergroups and private chats of bots with forum topic mode enabled only
            direct_messages_topic_id: Identifier of the direct messages topic to which the messages will be sent; required if the messages are sent to a direct messages chat
            media: A JSON-serialized Array describing messages to be sent, must include 2-10 items
            disable_notification: Sends messages silently. Users will receive a notification with no sound.
            protect_content: Protects the contents of the sent messages from forwarding and saving
            allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance.
            message_effect_id: Unique identifier of the message effect to be added to the message; for private chats only
            reply_parameters: Description of the message to reply to
        """
        return await self.call(SendMediaGroup(
            business_connection_id=business_connection_id,
            chat_id=chat_id,
            message_thread_id=message_thread_id,
            direct_messages_topic_id=direct_messages_topic_id,
            media=media,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters,
        ))

    async def send_location(
        self,
        chat_id: Union[int, str],
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
        """Use this method to send point on the map. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendlocation
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
            chat_id: Unique identifier for the target chat or username of the target bot, supergroup or channel in the format @username
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
        return await self.call(SendLocation(
            business_connection_id=business_connection_id,
            chat_id=chat_id,
            message_thread_id=message_thread_id,
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
        ))

    async def send_venue(
        self,
        chat_id: Union[int, str],
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
        """Use this method to send information about a venue. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendvenue
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
            chat_id: Unique identifier for the target chat or username of the target bot, supergroup or channel in the format @username
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
        return await self.call(SendVenue(
            business_connection_id=business_connection_id,
            chat_id=chat_id,
            message_thread_id=message_thread_id,
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
        ))

    async def send_contact(
        self,
        chat_id: Union[int, str],
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
        """Use this method to send phone contacts. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendcontact
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
            chat_id: Unique identifier for the target chat or username of the target bot, supergroup or channel in the format @username
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
        return await self.call(SendContact(
            business_connection_id=business_connection_id,
            chat_id=chat_id,
            message_thread_id=message_thread_id,
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
        ))

    async def send_poll(
        self,
        chat_id: Union[int, str],
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
        """Use this method to send a native poll. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendpoll
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
            chat_id: Unique identifier for the target chat or username of the target bot, supergroup or channel in the format @username. Polls can't be sent to channel direct messages chats.
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
        return await self.call(SendPoll(
            business_connection_id=business_connection_id,
            chat_id=chat_id,
            message_thread_id=message_thread_id,
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
        ))

    async def send_checklist(
        self,
        business_connection_id: str,
        chat_id: Union[int, str],
        checklist: InputChecklist,
        *,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ) -> Message:
        """Use this method to send a checklist on behalf of a connected business account. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendchecklist
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
            chat_id: Unique identifier for the target chat or username of the target bot in the format @username
            checklist: A JSON-serialized object for the checklist to send
            disable_notification: Sends the message silently. Users will receive a notification with no sound.
            protect_content: Protects the contents of the sent message from forwarding and saving
            message_effect_id: Unique identifier of the message effect to be added to the message
            reply_parameters: A JSON-serialized object for description of the message to reply to
            reply_markup: A JSON-serialized object for an inline keyboard
        """
        return await self.call(SendChecklist(
            business_connection_id=business_connection_id,
            chat_id=chat_id,
            checklist=checklist,
            disable_notification=disable_notification,
            protect_content=protect_content,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        ))

    async def send_dice(
        self,
        chat_id: Union[int, str],
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
        """Use this method to send an animated emoji that will display a random value. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#senddice
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
            chat_id: Unique identifier for the target chat or username of the target bot, supergroup or channel in the format @username
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
        return await self.call(SendDice(
            business_connection_id=business_connection_id,
            chat_id=chat_id,
            message_thread_id=message_thread_id,
            direct_messages_topic_id=direct_messages_topic_id,
            emoji=emoji,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        ))

    async def send_message_draft(
        self,
        chat_id: int,
        draft_id: int,
        *,
        message_thread_id: Optional[int] = None,
        text: Optional[str] = None,
        parse_mode: Optional[str] = None,
        entities: Optional[List[MessageEntity]] = None,
        can_stop: Optional[bool] = None,
        keep_on_stop: Optional[bool] = None,
    ) -> bool:
        """Use this method to stream a partial message to a user while the message is being generated. Note that the streamed draft is ephemeral and acts as a temporary 30-second preview - once the output is finalized, you must call sendMessage with the complete message to persist it in the user's chat. Returns True on success.
        
        https://core.telegram.org/bots/api#sendmessagedraft
        
        Args:
            chat_id: Unique identifier for the target private chat
            message_thread_id: Unique identifier for the target message thread
            draft_id: Unique identifier of the message draft; must be non-zero. Changes to drafts with the same identifier are animated. Otherwise, the draft is replaced without animation.
            text: Text of the message to be sent, 0-4096 characters after entities parsing. Pass an empty text to show a "Thinking..." placeholder.
            parse_mode: Mode for parsing entities in the message text. See formatting options for more details.
            entities: A JSON-serialized list of special entities that appear in message text, which can be specified instead of parse_mode
            can_stop: Pass True to show the user a button to stop further drafts. The bot will receive an Update "stopped_message_generation" if the user presses the button.
            keep_on_stop: Pass True to keep the draft in the chat when the button is pressed. The draft will still disappear after a short time or if the bot sends a message. To fully preserve the partial draft, the bot should send it as a new message.
        """
        return await self.call(SendMessageDraft(
            chat_id=chat_id,
            message_thread_id=message_thread_id,
            draft_id=draft_id,
            text=text,
            parse_mode=parse_mode,
            entities=entities,
            can_stop=can_stop,
            keep_on_stop=keep_on_stop,
        ))

    async def send_chat_action(
        self,
        chat_id: Union[int, str],
        action: str,
        *,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
    ) -> bool:
        """Use this method when you need to tell the user that something is happening on the bot's side. The status is set for 5 seconds or less (when a message arrives from your bot, Telegram clients clear its typing status). Returns True on success.
        
        We only recommend using this method when a response from the bot will take a noticeable amount of time to arrive.
        
        https://core.telegram.org/bots/api#sendchataction
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the action will be sent
            chat_id: Unique identifier for the target chat or username of the target bot or supergroup in the format @username. Channel chats and channel direct messages chats aren't supported.
            message_thread_id: Unique identifier for the target message thread or topic of a forum; for supergroups and private chats of bots with forum topic mode enabled only
            action: Type of action to broadcast. Choose one, depending on what the user is about to receive: typing for text messages, upload_photo for photos, record_video or upload_video for videos, record_voice or upload_voice for voice notes, upload_document for general files, choose_sticker for stickers, find_location for location data, record_video_note or upload_video_note for video notes.
        """
        return await self.call(SendChatAction(
            business_connection_id=business_connection_id,
            chat_id=chat_id,
            message_thread_id=message_thread_id,
            action=action,
        ))

    async def set_message_reaction(
        self,
        chat_id: Union[int, str],
        message_id: int,
        *,
        reaction: Optional[List[ReactionType]] = None,
        is_big: Optional[bool] = None,
    ) -> bool:
        """Use this method to change the chosen reactions on a message. Service messages of some types can't be reacted to. Automatically forwarded messages from a channel to its discussion group have the same available reactions as messages in the channel. Bots can't use paid reactions. Returns True on success.
        
        https://core.telegram.org/bots/api#setmessagereaction
        
        Args:
            chat_id: Unique identifier for the target chat or username of the target bot, supergroup or channel in the format @username
            message_id: Identifier of the target message. If the message belongs to a media group, the reaction is set to the first non-deleted message in the group instead.
            reaction: A JSON-serialized list of reaction types to set on the message. Currently, as non-premium users, bots can set up to one reaction per message. A custom emoji reaction can be used if it is either already present on the message or explicitly allowed by chat administrators. Paid reactions can't be used by bots.
            is_big: Pass True to set the reaction with a big animation
        """
        return await self.call(SetMessageReaction(
            chat_id=chat_id,
            message_id=message_id,
            reaction=reaction,
            is_big=is_big,
        ))

    async def get_user_profile_photos(
        self,
        user_id: int,
        *,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> UserProfilePhotos:
        """Use this method to get a list of profile pictures for a user. Returns a UserProfilePhotos object.
        
        https://core.telegram.org/bots/api#getuserprofilephotos
        
        Args:
            user_id: Unique identifier of the target user
            offset: Sequential number of the first photo to be returned. By default, all photos are returned.
            limit: Limits the number of photos to be retrieved. Values between 1-100 are accepted. Defaults to 100.
        """
        return await self.call(GetUserProfilePhotos(
            user_id=user_id,
            offset=offset,
            limit=limit,
        ))

    async def get_user_profile_audios(
        self,
        user_id: int,
        *,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> UserProfileAudios:
        """Use this method to get a list of profile audios for a user. Returns a UserProfileAudios object.
        
        https://core.telegram.org/bots/api#getuserprofileaudios
        
        Args:
            user_id: Unique identifier of the target user
            offset: Sequential number of the first audio to be returned. By default, all audios are returned.
            limit: Limits the number of audios to be retrieved. Values between 1-100 are accepted. Defaults to 100.
        """
        return await self.call(GetUserProfileAudios(
            user_id=user_id,
            offset=offset,
            limit=limit,
        ))

    async def set_user_emoji_status(
        self,
        user_id: int,
        *,
        emoji_status_custom_emoji_id: Optional[str] = None,
        emoji_status_expiration_date: Optional[int] = None,
    ) -> bool:
        """Changes the emoji status for a given user that previously allowed the bot to manage their emoji status via the Mini App method requestEmojiStatusAccess. Returns True on success.
        
        https://core.telegram.org/bots/api#setuseremojistatus
        
        Args:
            user_id: Unique identifier of the target user
            emoji_status_custom_emoji_id: Custom emoji identifier of the emoji status to set. Pass an empty string to remove the status.
            emoji_status_expiration_date: Expiration date of the emoji status, if any
        """
        return await self.call(SetUserEmojiStatus(
            user_id=user_id,
            emoji_status_custom_emoji_id=emoji_status_custom_emoji_id,
            emoji_status_expiration_date=emoji_status_expiration_date,
        ))

    async def get_file(
        self,
        file_id: str,
    ) -> File:
        """Use this method to get basic information about a file and prepare it for downloading. For the moment, bots can download files of up to 20MB in size. On success, a File object is returned. The file can then be downloaded via the link https://api.telegram.org/file/bot<token>/<file_path>, where <file_path> is taken from the response. It is guaranteed that the link will be valid for at least 1 hour. When the link expires, a new one can be requested by calling getFile again.
        
        Note: This function may not preserve the original file name and MIME type. You should save the file's MIME type and name (if available) when the File object is received.
        
        https://core.telegram.org/bots/api#getfile
        
        Args:
            file_id: File identifier to get information about
        """
        return await self.call(GetFile(
            file_id=file_id,
        ))

    async def ban_chat_member(
        self,
        chat_id: Union[int, str],
        user_id: int,
        *,
        until_date: Optional[int] = None,
        revoke_messages: Optional[bool] = None,
    ) -> bool:
        """Use this method to ban a user in a group, a supergroup or a channel. In the case of supergroups and channels, the user will not be able to return to the chat on their own using invite links, etc., unless unbanned first. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Returns True on success.
        
        https://core.telegram.org/bots/api#banchatmember
        
        Args:
            chat_id: Unique identifier for the target group or username of the target supergroup or channel in the format @username
            user_id: Unique identifier of the target user
            until_date: Date when the user will be unbanned; Unix time. If user is banned for more than 366 days or less than 30 seconds from the current time they are considered to be banned forever. Applied for supergroups and channels only.
            revoke_messages: Pass True to delete all messages from the chat for the user that is being removed. If False, the user will be able to see messages in the group that were sent before the user was removed. Always True for supergroups and channels.
        """
        return await self.call(BanChatMember(
            chat_id=chat_id,
            user_id=user_id,
            until_date=until_date,
            revoke_messages=revoke_messages,
        ))

    async def unban_chat_member(
        self,
        chat_id: Union[int, str],
        user_id: int,
        *,
        only_if_banned: Optional[bool] = None,
    ) -> bool:
        """Use this method to unban a previously banned user in a supergroup or channel. The user will not return to the group or channel automatically, but will be able to join via link, etc. The bot must be an administrator for this to work. By default, this method guarantees that after the call the user is not a member of the chat, but will be able to join it. So if the user is a member of the chat they will also be removed from the chat. If you don't want this, use the parameter only_if_banned. Returns True on success.
        
        https://core.telegram.org/bots/api#unbanchatmember
        
        Args:
            chat_id: Unique identifier for the target group or username of the target supergroup or channel in the format @username
            user_id: Unique identifier of the target user
            only_if_banned: Do nothing if the user is not banned
        """
        return await self.call(UnbanChatMember(
            chat_id=chat_id,
            user_id=user_id,
            only_if_banned=only_if_banned,
        ))

    async def restrict_chat_member(
        self,
        chat_id: Union[int, str],
        user_id: int,
        permissions: ChatPermissions,
        *,
        use_independent_chat_permissions: Optional[bool] = None,
        until_date: Optional[int] = None,
    ) -> bool:
        """Use this method to restrict a user in a supergroup. The bot must be an administrator in the supergroup for this to work and must have the appropriate administrator rights. Pass True for all permissions to lift restrictions from a user. Returns True on success.
        
        https://core.telegram.org/bots/api#restrictchatmember
        
        Args:
            chat_id: Unique identifier for the target chat or username of the target supergroup in the format @username
            user_id: Unique identifier of the target user
            permissions: A JSON-serialized object for new user permissions
            use_independent_chat_permissions: Pass True if chat permissions are set independently. Otherwise, the can_send_other_messages and can_add_web_page_previews permissions will imply the can_send_messages, can_send_audios, can_send_documents, can_send_photos, can_send_videos, can_send_video_notes, and can_send_voice_notes permissions; the can_send_polls permission will imply the can_send_messages permission.
            until_date: Date when restrictions will be lifted for the user; Unix time. If user is restricted for more than 366 days or less than 30 seconds from the current time, they are considered to be restricted forever.
        """
        return await self.call(RestrictChatMember(
            chat_id=chat_id,
            user_id=user_id,
            permissions=permissions,
            use_independent_chat_permissions=use_independent_chat_permissions,
            until_date=until_date,
        ))

    async def promote_chat_member(
        self,
        chat_id: Union[int, str],
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
        """Use this method to promote or demote a user in a supergroup or a channel. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Pass False for all boolean parameters to demote a user. Returns True on success.
        
        https://core.telegram.org/bots/api#promotechatmember
        
        Args:
            chat_id: Unique identifier for the target chat or username of the target channel in the format @username
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
        return await self.call(PromoteChatMember(
            chat_id=chat_id,
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
        ))

    async def set_chat_administrator_custom_title(
        self,
        chat_id: Union[int, str],
        user_id: int,
        custom_title: str,
    ) -> bool:
        """Use this method to set a custom title for an administrator in a supergroup promoted by the bot. Returns True on success.
        
        https://core.telegram.org/bots/api#setchatadministratorcustomtitle
        
        Args:
            chat_id: Unique identifier for the target chat or username of the target supergroup in the format @username
            user_id: Unique identifier of the target user
            custom_title: New custom title for the administrator; 0-16 characters, emoji are not allowed
        """
        return await self.call(SetChatAdministratorCustomTitle(
            chat_id=chat_id,
            user_id=user_id,
            custom_title=custom_title,
        ))

    async def set_chat_member_tag(
        self,
        chat_id: Union[int, str],
        user_id: int,
        *,
        tag: Optional[str] = None,
    ) -> bool:
        """Use this method to set a tag for a regular member in a group or a supergroup. The bot must be an administrator in the chat for this to work and must have the can_manage_tags administrator right. Returns True on success.
        
        https://core.telegram.org/bots/api#setchatmembertag
        
        Args:
            chat_id: Unique identifier for the target chat or username of the target supergroup in the format @username
            user_id: Unique identifier of the target user
            tag: New tag for the member; 0-16 characters, emoji are not allowed
        """
        return await self.call(SetChatMemberTag(
            chat_id=chat_id,
            user_id=user_id,
            tag=tag,
        ))

    async def ban_chat_sender_chat(
        self,
        chat_id: Union[int, str],
        sender_chat_id: int,
    ) -> bool:
        """Use this method to ban a channel chat in a supergroup or a channel. Until the chat is unbanned, the owner of the banned chat won't be able to send messages on behalf of any of their channels. The bot must be an administrator in the supergroup or channel for this to work and must have the appropriate administrator rights. Returns True on success.
        
        https://core.telegram.org/bots/api#banchatsenderchat
        
        Args:
            chat_id: Unique identifier for the target chat or username of the target channel in the format @username
            sender_chat_id: Unique identifier of the target sender chat
        """
        return await self.call(BanChatSenderChat(
            chat_id=chat_id,
            sender_chat_id=sender_chat_id,
        ))

    async def unban_chat_sender_chat(
        self,
        chat_id: Union[int, str],
        sender_chat_id: int,
    ) -> bool:
        """Use this method to unban a previously banned channel chat in a supergroup or channel. The bot must be an administrator for this to work and must have the appropriate administrator rights. Returns True on success.
        
        https://core.telegram.org/bots/api#unbanchatsenderchat
        
        Args:
            chat_id: Unique identifier for the target chat or username of the target channel in the format @username
            sender_chat_id: Unique identifier of the target sender chat
        """
        return await self.call(UnbanChatSenderChat(
            chat_id=chat_id,
            sender_chat_id=sender_chat_id,
        ))

    async def set_chat_permissions(
        self,
        chat_id: Union[int, str],
        permissions: ChatPermissions,
        *,
        use_independent_chat_permissions: Optional[bool] = None,
    ) -> bool:
        """Use this method to set default chat permissions for all members. The bot must be an administrator in the group or a supergroup for this to work and must have the can_restrict_members administrator rights. Returns True on success.
        
        https://core.telegram.org/bots/api#setchatpermissions
        
        Args:
            chat_id: Unique identifier for the target chat or username of the target supergroup in the format @username
            permissions: A JSON-serialized object for new default chat permissions
            use_independent_chat_permissions: Pass True if chat permissions are set independently. Otherwise, the can_send_other_messages and can_add_web_page_previews permissions will imply the can_send_messages, can_send_audios, can_send_documents, can_send_photos, can_send_videos, can_send_video_notes, and can_send_voice_notes permissions; the can_send_polls permission will imply the can_send_messages permission.
        """
        return await self.call(SetChatPermissions(
            chat_id=chat_id,
            permissions=permissions,
            use_independent_chat_permissions=use_independent_chat_permissions,
        ))

    async def export_chat_invite_link(
        self,
        chat_id: Union[int, str],
    ) -> str:
        """Use this method to generate a new primary invite link for a chat; any previously generated primary link is revoked. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Returns the new invite link as String on success.
        
        https://core.telegram.org/bots/api#exportchatinvitelink
        
        Args:
            chat_id: Unique identifier for the target chat or username of the target channel in the format @username
        """
        return await self.call(ExportChatInviteLink(
            chat_id=chat_id,
        ))

    async def create_chat_invite_link(
        self,
        chat_id: Union[int, str],
        *,
        name: Optional[str] = None,
        expire_date: Optional[int] = None,
        member_limit: Optional[int] = None,
        creates_join_request: Optional[bool] = None,
    ) -> ChatInviteLink:
        """Use this method to create an additional invite link for a chat. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. The link can be revoked using the method revokeChatInviteLink. Returns the new invite link as ChatInviteLink object.
        
        https://core.telegram.org/bots/api#createchatinvitelink
        
        Args:
            chat_id: Unique identifier for the target chat or username of the target channel in the format @username
            name: Invite link name; 0-32 characters
            expire_date: Point in time (Unix timestamp) when the link will expire
            member_limit: The maximum number of users that can be members of the chat simultaneously after joining the chat via this invite link; 1-99999
            creates_join_request: True, if users joining the chat via the link need to be approved by chat administrators. If True, member_limit can't be specified.
        """
        return await self.call(CreateChatInviteLink(
            chat_id=chat_id,
            name=name,
            expire_date=expire_date,
            member_limit=member_limit,
            creates_join_request=creates_join_request,
        ))

    async def edit_chat_invite_link(
        self,
        chat_id: Union[int, str],
        invite_link: str,
        *,
        name: Optional[str] = None,
        expire_date: Optional[int] = None,
        member_limit: Optional[int] = None,
        creates_join_request: Optional[bool] = None,
    ) -> ChatInviteLink:
        """Use this method to edit a non-primary invite link created by the bot. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Returns the edited invite link as a ChatInviteLink object.
        
        https://core.telegram.org/bots/api#editchatinvitelink
        
        Args:
            chat_id: Unique identifier for the target chat or username of the target channel in the format @username
            invite_link: The invite link to edit
            name: Invite link name; 0-32 characters
            expire_date: Point in time (Unix timestamp) when the link will expire
            member_limit: The maximum number of users that can be members of the chat simultaneously after joining the chat via this invite link; 1-99999
            creates_join_request: True, if users joining the chat via the link need to be approved by chat administrators. If True, member_limit can't be specified.
        """
        return await self.call(EditChatInviteLink(
            chat_id=chat_id,
            invite_link=invite_link,
            name=name,
            expire_date=expire_date,
            member_limit=member_limit,
            creates_join_request=creates_join_request,
        ))

    async def create_chat_subscription_invite_link(
        self,
        chat_id: Union[int, str],
        subscription_period: int,
        subscription_price: int,
        *,
        name: Optional[str] = None,
    ) -> ChatInviteLink:
        """Use this method to create a subscription invite link for a channel chat. The bot must have the can_invite_users administrator rights. The link can be edited using the method editChatSubscriptionInviteLink or revoked using the method revokeChatInviteLink. Returns the new invite link as a ChatInviteLink object.
        
        https://core.telegram.org/bots/api#createchatsubscriptioninvitelink
        
        Args:
            chat_id: Unique identifier for the target channel chat or username of the target channel in the format @username
            name: Invite link name; 0-32 characters
            subscription_period: The number of seconds the subscription will be active for before the next payment. Currently, it must always be 2592000 (30 days).
            subscription_price: The amount of Telegram Stars a user must pay initially and after each subsequent subscription period to be a member of the chat; 1-10000
        """
        return await self.call(CreateChatSubscriptionInviteLink(
            chat_id=chat_id,
            name=name,
            subscription_period=subscription_period,
            subscription_price=subscription_price,
        ))

    async def edit_chat_subscription_invite_link(
        self,
        chat_id: Union[int, str],
        invite_link: str,
        *,
        name: Optional[str] = None,
    ) -> ChatInviteLink:
        """Use this method to edit a subscription invite link created by the bot. The bot must have the can_invite_users administrator rights. Returns the edited invite link as a ChatInviteLink object.
        
        https://core.telegram.org/bots/api#editchatsubscriptioninvitelink
        
        Args:
            chat_id: Unique identifier for the target chat or username of the target channel in the format @username
            invite_link: The invite link to edit
            name: Invite link name; 0-32 characters
        """
        return await self.call(EditChatSubscriptionInviteLink(
            chat_id=chat_id,
            invite_link=invite_link,
            name=name,
        ))

    async def revoke_chat_invite_link(
        self,
        chat_id: Union[int, str],
        invite_link: str,
    ) -> ChatInviteLink:
        """Use this method to revoke an invite link created by the bot. If the primary link is revoked, a new link is automatically generated. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Returns the revoked invite link as ChatInviteLink object.
        
        https://core.telegram.org/bots/api#revokechatinvitelink
        
        Args:
            chat_id: Unique identifier of the target chat or username of the target channel in the format @username
            invite_link: The invite link to revoke
        """
        return await self.call(RevokeChatInviteLink(
            chat_id=chat_id,
            invite_link=invite_link,
        ))

    async def approve_chat_join_request(
        self,
        chat_id: Union[int, str],
        user_id: int,
    ) -> bool:
        """Use this method to approve a chat join request. The bot must be an administrator in the chat for this to work and must have the can_invite_users administrator right. Returns True on success.
        
        https://core.telegram.org/bots/api#approvechatjoinrequest
        
        Args:
            chat_id: Unique identifier for the target chat or username of the target channel in the format @username
            user_id: Unique identifier of the target user
        """
        return await self.call(ApproveChatJoinRequest(
            chat_id=chat_id,
            user_id=user_id,
        ))

    async def decline_chat_join_request(
        self,
        chat_id: Union[int, str],
        user_id: int,
    ) -> bool:
        """Use this method to decline a chat join request. The bot must be an administrator in the chat for this to work and must have the can_invite_users administrator right. Returns True on success.
        
        https://core.telegram.org/bots/api#declinechatjoinrequest
        
        Args:
            chat_id: Unique identifier for the target chat or username of the target channel in the format @username
            user_id: Unique identifier of the target user
        """
        return await self.call(DeclineChatJoinRequest(
            chat_id=chat_id,
            user_id=user_id,
        ))

    async def answer_chat_join_request_query(
        self,
        chat_join_request_query_id: str,
        result: str,
    ) -> bool:
        """Use this method to process a received chat join request query. Returns True on success.
        
        https://core.telegram.org/bots/api#answerchatjoinrequestquery
        
        Args:
            chat_join_request_query_id: Unique identifier of the join request query
            result: Result of the query. Must be either "approve" to allow the user to join the chat, "decline" to disallow the user to join the chat, or "queue" to leave the decision to other administrators.
        """
        return await self.call(AnswerChatJoinRequestQuery(
            chat_join_request_query_id=chat_join_request_query_id,
            result=result,
        ))

    async def send_chat_join_request_web_app(
        self,
        chat_join_request_query_id: str,
        web_app_url: str,
    ) -> bool:
        """Use this method to process a received chat join request query by showing a Mini App to the user before deciding the outcome. Call answerChatJoinRequestQuery to resolve the join request query based on the user interaction with the Mini App. Returns True on success.
        
        https://core.telegram.org/bots/api#sendchatjoinrequestwebapp
        
        Args:
            chat_join_request_query_id: Unique identifier of the join request query
            web_app_url: An HTTPS URL of a Web App to be opened with additional data as specified in Initializing Web Apps
        """
        return await self.call(SendChatJoinRequestWebApp(
            chat_join_request_query_id=chat_join_request_query_id,
            web_app_url=web_app_url,
        ))

    async def set_chat_photo(
        self,
        chat_id: Union[int, str],
        photo: InputFile,
    ) -> bool:
        """Use this method to set a new profile photo for the chat. Photos can't be changed for private chats. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Returns True on success.
        
        https://core.telegram.org/bots/api#setchatphoto
        
        Args:
            chat_id: Unique identifier for the target chat or username of the target channel in the format @username
            photo: New chat photo, uploaded using multipart/form-data
        """
        return await self.call(SetChatPhoto(
            chat_id=chat_id,
            photo=photo,
        ))

    async def delete_chat_photo(
        self,
        chat_id: Union[int, str],
    ) -> bool:
        """Use this method to delete a chat photo. Photos can't be changed for private chats. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Returns True on success.
        
        https://core.telegram.org/bots/api#deletechatphoto
        
        Args:
            chat_id: Unique identifier for the target chat or username of the target channel in the format @username
        """
        return await self.call(DeleteChatPhoto(
            chat_id=chat_id,
        ))

    async def set_chat_title(
        self,
        chat_id: Union[int, str],
        title: str,
    ) -> bool:
        """Use this method to change the title of a chat. Titles can't be changed for private chats. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Returns True on success.
        
        https://core.telegram.org/bots/api#setchattitle
        
        Args:
            chat_id: Unique identifier for the target chat or username of the target channel in the format @username
            title: New chat title, 1-128 characters
        """
        return await self.call(SetChatTitle(
            chat_id=chat_id,
            title=title,
        ))

    async def set_chat_description(
        self,
        chat_id: Union[int, str],
        *,
        description: Optional[str] = None,
    ) -> bool:
        """Use this method to change the description of a group, a supergroup or a channel. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Returns True on success.
        
        https://core.telegram.org/bots/api#setchatdescription
        
        Args:
            chat_id: Unique identifier for the target chat or username of the target channel in the format @username
            description: New chat description, 0-255 characters
        """
        return await self.call(SetChatDescription(
            chat_id=chat_id,
            description=description,
        ))

    async def pin_chat_message(
        self,
        chat_id: Union[int, str],
        message_id: int,
        *,
        business_connection_id: Optional[str] = None,
        disable_notification: Optional[bool] = None,
    ) -> bool:
        """Use this method to add a message to the list of pinned messages in a chat. In private chats and channel direct messages chats, all non-service messages can be pinned. Conversely, the bot must be an administrator with the 'can_pin_messages' right or the 'can_edit_messages' right to pin messages in groups and channels respectively. Returns True on success.
        
        https://core.telegram.org/bots/api#pinchatmessage
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message will be pinned
            chat_id: Unique identifier for the target chat or username of the target channel in the format @username
            message_id: Identifier of a message to pin
            disable_notification: Pass True if it is not necessary to send a notification to all chat members about the new pinned message. Notifications are always disabled in channels and private chats.
        """
        return await self.call(PinChatMessage(
            business_connection_id=business_connection_id,
            chat_id=chat_id,
            message_id=message_id,
            disable_notification=disable_notification,
        ))

    async def unpin_chat_message(
        self,
        chat_id: Union[int, str],
        *,
        business_connection_id: Optional[str] = None,
        message_id: Optional[int] = None,
    ) -> bool:
        """Use this method to remove a message from the list of pinned messages in a chat. In private chats and channel direct messages chats, all messages can be unpinned. Conversely, the bot must be an administrator with the 'can_pin_messages' right or the 'can_edit_messages' right to unpin messages in groups and channels respectively. Returns True on success.
        
        https://core.telegram.org/bots/api#unpinchatmessage
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message will be unpinned
            chat_id: Unique identifier for the target chat or username of the target channel in the format @username
            message_id: Identifier of the message to unpin. Required if business_connection_id is specified. If not specified, the most recent pinned message (by sending date) will be unpinned.
        """
        return await self.call(UnpinChatMessage(
            business_connection_id=business_connection_id,
            chat_id=chat_id,
            message_id=message_id,
        ))

    async def unpin_all_chat_messages(
        self,
        chat_id: Union[int, str],
    ) -> bool:
        """Use this method to clear the list of pinned messages in a chat. In private chats and channel direct messages chats, no additional rights are required to unpin all pinned messages. Conversely, the bot must be an administrator with the 'can_pin_messages' right or the 'can_edit_messages' right to unpin all pinned messages in groups and channels respectively. Returns True on success.
        
        https://core.telegram.org/bots/api#unpinallchatmessages
        
        Args:
            chat_id: Unique identifier for the target chat or username of the target channel in the format @username
        """
        return await self.call(UnpinAllChatMessages(
            chat_id=chat_id,
        ))

    async def leave_chat(
        self,
        chat_id: Union[int, str],
    ) -> bool:
        """Use this method for your bot to leave a group, supergroup or channel. Returns True on success.
        
        https://core.telegram.org/bots/api#leavechat
        
        Args:
            chat_id: Unique identifier for the target chat or username of the target supergroup or channel in the format @username. Channel direct messages chats aren't supported; leave the corresponding channel instead.
        """
        return await self.call(LeaveChat(
            chat_id=chat_id,
        ))

    async def get_chat(
        self,
        chat_id: Union[int, str],
    ) -> ChatFullInfo:
        """Use this method to get up-to-date information about the chat. Returns a ChatFullInfo object on success.
        
        https://core.telegram.org/bots/api#getchat
        
        Args:
            chat_id: Unique identifier for the target chat or username of the target supergroup or channel in the format @username
        """
        return await self.call(GetChat(
            chat_id=chat_id,
        ))

    async def get_chat_administrators(
        self,
        chat_id: Union[int, str],
        *,
        return_bots: Optional[bool] = None,
    ) -> List[ChatMember]:
        """Use this method to get a list of administrators in a chat. Returns an Array of ChatMember objects.
        
        https://core.telegram.org/bots/api#getchatadministrators
        
        Args:
            chat_id: Unique identifier for the target chat or username of the target supergroup or channel in the format @username
            return_bots: Pass True to additionally receive all bots that are administrators of the chat. By default, bots other than the current bot are omitted.
        """
        return await self.call(GetChatAdministrators(
            chat_id=chat_id,
            return_bots=return_bots,
        ))

    async def get_chat_member_count(
        self,
        chat_id: Union[int, str],
    ) -> int:
        """Use this method to get the number of members in a chat. Returns Integer on success.
        
        https://core.telegram.org/bots/api#getchatmembercount
        
        Args:
            chat_id: Unique identifier for the target chat or username of the target supergroup or channel in the format @username
        """
        return await self.call(GetChatMemberCount(
            chat_id=chat_id,
        ))

    async def get_chat_member(
        self,
        chat_id: Union[int, str],
        user_id: int,
    ) -> ChatMember:
        """Use this method to get information about a member of a chat. The method is only guaranteed to work for other users if the bot is an administrator in the chat. Returns a ChatMember object on success.
        
        https://core.telegram.org/bots/api#getchatmember
        
        Args:
            chat_id: Unique identifier for the target chat or username of the target supergroup or channel in the format @username
            user_id: Unique identifier of the target user
        """
        return await self.call(GetChatMember(
            chat_id=chat_id,
            user_id=user_id,
        ))

    async def get_user_personal_chat_messages(
        self,
        user_id: int,
        limit: int,
    ) -> List[Message]:
        """Use this method to get the last messages from the personal chat (i.e., the chat currently added to their profile) of a given user. On success, an Array of Message objects is returned.
        
        https://core.telegram.org/bots/api#getuserpersonalchatmessages
        
        Args:
            user_id: Unique identifier for the target user
            limit: The maximum number of messages to return; 1-20
        """
        return await self.call(GetUserPersonalChatMessages(
            user_id=user_id,
            limit=limit,
        ))

    async def set_chat_sticker_set(
        self,
        chat_id: Union[int, str],
        sticker_set_name: str,
    ) -> bool:
        """Use this method to set a new group sticker set for a supergroup. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Use the field can_set_sticker_set optionally returned in getChat requests to check if the bot can use this method. Returns True on success.
        
        https://core.telegram.org/bots/api#setchatstickerset
        
        Args:
            chat_id: Unique identifier for the target chat or username of the target supergroup in the format @username
            sticker_set_name: Name of the sticker set to be set as the group sticker set
        """
        return await self.call(SetChatStickerSet(
            chat_id=chat_id,
            sticker_set_name=sticker_set_name,
        ))

    async def delete_chat_sticker_set(
        self,
        chat_id: Union[int, str],
    ) -> bool:
        """Use this method to delete a group sticker set from a supergroup. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Use the field can_set_sticker_set optionally returned in getChat requests to check if the bot can use this method. Returns True on success.
        
        https://core.telegram.org/bots/api#deletechatstickerset
        
        Args:
            chat_id: Unique identifier for the target chat or username of the target supergroup in the format @username
        """
        return await self.call(DeleteChatStickerSet(
            chat_id=chat_id,
        ))

    async def get_forum_topic_icon_stickers(
        self,
    ) -> List[Sticker]:
        """Use this method to get custom emoji stickers, which can be used as a forum topic icon by any user. Requires no parameters. Returns an Array of Sticker objects.
        
        https://core.telegram.org/bots/api#getforumtopiciconstickers
        """
        return await self.call(GetForumTopicIconStickers(
        ))

    async def create_forum_topic(
        self,
        chat_id: Union[int, str],
        name: str,
        *,
        icon_color: Optional[int] = None,
        icon_custom_emoji_id: Optional[str] = None,
    ) -> ForumTopic:
        """Use this method to create a topic in a forum supergroup chat or a private chat with a user. In the case of a supergroup chat the bot must be an administrator in the chat for this to work and must have the can_manage_topics administrator right. Returns information about the created topic as a ForumTopic object.
        
        https://core.telegram.org/bots/api#createforumtopic
        
        Args:
            chat_id: Unique identifier for the target chat or username of the target supergroup in the format @username
            name: Topic name, 1-128 characters
            icon_color: Color of the topic icon in RGB format. Currently, must be one of 7322096 (0x6FB9F0), 16766590 (0xFFD67E), 13338331 (0xCB86DB), 9367192 (0x8EEE98), 16749490 (0xFF93B2), or 16478047 (0xFB6F5F).
            icon_custom_emoji_id: Unique identifier of the custom emoji shown as the topic icon. Use getForumTopicIconStickers to get all allowed custom emoji identifiers.
        """
        return await self.call(CreateForumTopic(
            chat_id=chat_id,
            name=name,
            icon_color=icon_color,
            icon_custom_emoji_id=icon_custom_emoji_id,
        ))

    async def edit_forum_topic(
        self,
        chat_id: Union[int, str],
        message_thread_id: int,
        *,
        name: Optional[str] = None,
        icon_custom_emoji_id: Optional[str] = None,
    ) -> bool:
        """Use this method to edit name and icon of a topic in a forum supergroup chat or a private chat with a user. In the case of a supergroup chat the bot must be an administrator in the chat for this to work and must have the can_manage_topics administrator rights, unless it is the creator of the topic. Returns True on success.
        
        https://core.telegram.org/bots/api#editforumtopic
        
        Args:
            chat_id: Unique identifier for the target chat or username of the target supergroup in the format @username
            message_thread_id: Unique identifier for the target message thread of the forum topic
            name: New topic name, 0-128 characters. If not specified or empty, the current name of the topic will be kept.
            icon_custom_emoji_id: New unique identifier of the custom emoji shown as the topic icon. Use getForumTopicIconStickers to get all allowed custom emoji identifiers. Pass an empty string to remove the icon. If not specified, the current icon will be kept.
        """
        return await self.call(EditForumTopic(
            chat_id=chat_id,
            message_thread_id=message_thread_id,
            name=name,
            icon_custom_emoji_id=icon_custom_emoji_id,
        ))

    async def close_forum_topic(
        self,
        chat_id: Union[int, str],
        message_thread_id: int,
    ) -> bool:
        """Use this method to close an open topic in a forum supergroup chat. The bot must be an administrator in the chat for this to work and must have the can_manage_topics administrator rights, unless it is the creator of the topic. Returns True on success.
        
        https://core.telegram.org/bots/api#closeforumtopic
        
        Args:
            chat_id: Unique identifier for the target chat or username of the target supergroup in the format @username
            message_thread_id: Unique identifier for the target message thread of the forum topic
        """
        return await self.call(CloseForumTopic(
            chat_id=chat_id,
            message_thread_id=message_thread_id,
        ))

    async def reopen_forum_topic(
        self,
        chat_id: Union[int, str],
        message_thread_id: int,
    ) -> bool:
        """Use this method to reopen a closed topic in a forum supergroup chat. The bot must be an administrator in the chat for this to work and must have the can_manage_topics administrator rights, unless it is the creator of the topic. Returns True on success.
        
        https://core.telegram.org/bots/api#reopenforumtopic
        
        Args:
            chat_id: Unique identifier for the target chat or username of the target supergroup in the format @username
            message_thread_id: Unique identifier for the target message thread of the forum topic
        """
        return await self.call(ReopenForumTopic(
            chat_id=chat_id,
            message_thread_id=message_thread_id,
        ))

    async def delete_forum_topic(
        self,
        chat_id: Union[int, str],
        message_thread_id: int,
    ) -> bool:
        """Use this method to delete a forum topic along with all its messages in a forum supergroup chat or a private chat with a user. In the case of a supergroup chat the bot must be an administrator in the chat for this to work and must have the can_delete_messages administrator rights. Returns True on success.
        
        https://core.telegram.org/bots/api#deleteforumtopic
        
        Args:
            chat_id: Unique identifier for the target chat or username of the target supergroup in the format @username
            message_thread_id: Unique identifier for the target message thread of the forum topic
        """
        return await self.call(DeleteForumTopic(
            chat_id=chat_id,
            message_thread_id=message_thread_id,
        ))

    async def unpin_all_forum_topic_messages(
        self,
        chat_id: Union[int, str],
        message_thread_id: int,
    ) -> bool:
        """Use this method to clear the list of pinned messages in a forum topic in a forum supergroup chat or a private chat with a user. In the case of a supergroup chat the bot must be an administrator in the chat for this to work and must have the can_pin_messages administrator right in the supergroup. Returns True on success.
        
        https://core.telegram.org/bots/api#unpinallforumtopicmessages
        
        Args:
            chat_id: Unique identifier for the target chat or username of the target supergroup in the format @username
            message_thread_id: Unique identifier for the target message thread of the forum topic
        """
        return await self.call(UnpinAllForumTopicMessages(
            chat_id=chat_id,
            message_thread_id=message_thread_id,
        ))

    async def edit_general_forum_topic(
        self,
        chat_id: Union[int, str],
        name: str,
    ) -> bool:
        """Use this method to edit the name of the 'General' topic in a forum supergroup chat. The bot must be an administrator in the chat for this to work and must have the can_manage_topics administrator rights. Returns True on success.
        
        https://core.telegram.org/bots/api#editgeneralforumtopic
        
        Args:
            chat_id: Unique identifier for the target chat or username of the target supergroup in the format @username
            name: New topic name, 1-128 characters
        """
        return await self.call(EditGeneralForumTopic(
            chat_id=chat_id,
            name=name,
        ))

    async def close_general_forum_topic(
        self,
        chat_id: Union[int, str],
    ) -> bool:
        """Use this method to close an open 'General' topic in a forum supergroup chat. The bot must be an administrator in the chat for this to work and must have the can_manage_topics administrator rights. Returns True on success.
        
        https://core.telegram.org/bots/api#closegeneralforumtopic
        
        Args:
            chat_id: Unique identifier for the target chat or username of the target supergroup in the format @username
        """
        return await self.call(CloseGeneralForumTopic(
            chat_id=chat_id,
        ))

    async def reopen_general_forum_topic(
        self,
        chat_id: Union[int, str],
    ) -> bool:
        """Use this method to reopen a closed 'General' topic in a forum supergroup chat. The bot must be an administrator in the chat for this to work and must have the can_manage_topics administrator rights. The topic will be automatically unhidden if it was hidden. Returns True on success.
        
        https://core.telegram.org/bots/api#reopengeneralforumtopic
        
        Args:
            chat_id: Unique identifier for the target chat or username of the target supergroup in the format @username
        """
        return await self.call(ReopenGeneralForumTopic(
            chat_id=chat_id,
        ))

    async def hide_general_forum_topic(
        self,
        chat_id: Union[int, str],
    ) -> bool:
        """Use this method to hide the 'General' topic in a forum supergroup chat. The bot must be an administrator in the chat for this to work and must have the can_manage_topics administrator rights. The topic will be automatically closed if it was open. Returns True on success.
        
        https://core.telegram.org/bots/api#hidegeneralforumtopic
        
        Args:
            chat_id: Unique identifier for the target chat or username of the target supergroup in the format @username
        """
        return await self.call(HideGeneralForumTopic(
            chat_id=chat_id,
        ))

    async def unhide_general_forum_topic(
        self,
        chat_id: Union[int, str],
    ) -> bool:
        """Use this method to unhide the 'General' topic in a forum supergroup chat. The bot must be an administrator in the chat for this to work and must have the can_manage_topics administrator rights. Returns True on success.
        
        https://core.telegram.org/bots/api#unhidegeneralforumtopic
        
        Args:
            chat_id: Unique identifier for the target chat or username of the target supergroup in the format @username
        """
        return await self.call(UnhideGeneralForumTopic(
            chat_id=chat_id,
        ))

    async def unpin_all_general_forum_topic_messages(
        self,
        chat_id: Union[int, str],
    ) -> bool:
        """Use this method to clear the list of pinned messages in a General forum topic. The bot must be an administrator in the chat for this to work and must have the can_pin_messages administrator right in the supergroup. Returns True on success.
        
        https://core.telegram.org/bots/api#unpinallgeneralforumtopicmessages
        
        Args:
            chat_id: Unique identifier for the target chat or username of the target supergroup in the format @username
        """
        return await self.call(UnpinAllGeneralForumTopicMessages(
            chat_id=chat_id,
        ))

    async def answer_callback_query(
        self,
        callback_query_id: str,
        *,
        text: Optional[str] = None,
        show_alert: Optional[bool] = None,
        url: Optional[str] = None,
        cache_time: Optional[int] = None,
    ) -> bool:
        """Use this method to send answers to callback queries sent from inline keyboards. The answer will be displayed to the user as a notification at the top of the chat screen or as an alert. On success, True is returned.
        
        https://core.telegram.org/bots/api#answercallbackquery
        
        Args:
            callback_query_id: Unique identifier for the query to be answered
            text: Text of the notification. If not specified, nothing will be shown to the user, 0-200 characters.
            show_alert: If True, an alert will be shown by the client instead of a notification at the top of the chat screen. Defaults to False.
            url: URL that will be opened by the user's client. If you have created a Game and accepted the conditions via @BotFather, specify the URL that opens your game - note that this will only work if the query comes from a callback_game button. Otherwise, you may use links like t.me/your_bot?start=XXXX that open your bot with a parameter.
            cache_time: The maximum amount of time in seconds that the result of the callback query may be cached client-side. Defaults to 0.
        """
        return await self.call(AnswerCallbackQuery(
            callback_query_id=callback_query_id,
            text=text,
            show_alert=show_alert,
            url=url,
            cache_time=cache_time,
        ))

    async def answer_guest_query(
        self,
        guest_query_id: str,
        result: InlineQueryResult,
    ) -> SentGuestMessage:
        """Use this method to reply to a received guest message. On success, a SentGuestMessage object is returned.
        
        https://core.telegram.org/bots/api#answerguestquery
        
        Args:
            guest_query_id: Unique identifier for the query to be answered
            result: A JSON-serialized object describing the message to be sent
        """
        return await self.call(AnswerGuestQuery(
            guest_query_id=guest_query_id,
            result=result,
        ))

    async def get_user_chat_boosts(
        self,
        chat_id: Union[int, str],
        user_id: int,
    ) -> UserChatBoosts:
        """Use this method to get the list of boosts added to a chat by a user. Requires administrator rights in the chat. Returns a UserChatBoosts object.
        
        https://core.telegram.org/bots/api#getuserchatboosts
        
        Args:
            chat_id: Unique identifier for the chat or username of the channel in the format @username
            user_id: Unique identifier of the target user
        """
        return await self.call(GetUserChatBoosts(
            chat_id=chat_id,
            user_id=user_id,
        ))

    async def get_business_connection(
        self,
        business_connection_id: str,
    ) -> BusinessConnection:
        """Use this method to get information about the connection of the bot with a business account. Returns a BusinessConnection object on success.
        
        https://core.telegram.org/bots/api#getbusinessconnection
        
        Args:
            business_connection_id: Unique identifier of the business connection
        """
        return await self.call(GetBusinessConnection(
            business_connection_id=business_connection_id,
        ))

    async def get_managed_bot_token(
        self,
        user_id: int,
    ) -> str:
        """Use this method to get the token of a managed bot. Returns the token as String on success.
        
        https://core.telegram.org/bots/api#getmanagedbottoken
        
        Args:
            user_id: User identifier of the managed bot whose token will be returned
        """
        return await self.call(GetManagedBotToken(
            user_id=user_id,
        ))

    async def replace_managed_bot_token(
        self,
        user_id: int,
    ) -> str:
        """Use this method to revoke the current token of a managed bot and generate a new one. Returns the new token as String on success.
        
        https://core.telegram.org/bots/api#replacemanagedbottoken
        
        Args:
            user_id: User identifier of the managed bot whose token will be replaced
        """
        return await self.call(ReplaceManagedBotToken(
            user_id=user_id,
        ))

    async def get_managed_bot_access_settings(
        self,
        user_id: int,
    ) -> BotAccessSettings:
        """Use this method to get the access settings of a managed bot. Returns a BotAccessSettings object on success.
        
        https://core.telegram.org/bots/api#getmanagedbotaccesssettings
        
        Args:
            user_id: User identifier of the managed bot whose access settings will be returned
        """
        return await self.call(GetManagedBotAccessSettings(
            user_id=user_id,
        ))

    async def set_managed_bot_access_settings(
        self,
        user_id: int,
        is_access_restricted: bool,
        *,
        added_user_ids: Optional[List[int]] = None,
    ) -> bool:
        """Use this method to change the access settings of a managed bot. Returns True on success.
        
        https://core.telegram.org/bots/api#setmanagedbotaccesssettings
        
        Args:
            user_id: User identifier of the managed bot whose access settings will be changed
            is_access_restricted: Pass True if only selected users can access the bot. The bot's owner can always access it.
            added_user_ids: A JSON-serialized list of up to 10 identifiers of users who will have access to the bot in addition to its owner. Ignored if is_access_restricted is False.
        """
        return await self.call(SetManagedBotAccessSettings(
            user_id=user_id,
            is_access_restricted=is_access_restricted,
            added_user_ids=added_user_ids,
        ))

    async def set_my_commands(
        self,
        commands: List[BotCommand],
        *,
        scope: Optional[BotCommandScope] = None,
        language_code: Optional[str] = None,
    ) -> bool:
        """Use this method to change the list of the bot's commands. See this manual for more details about bot commands. Returns True on success.
        
        https://core.telegram.org/bots/api#setmycommands
        
        Args:
            commands: A JSON-serialized list of bot commands to be set as the list of the bot's commands. At most 100 commands can be specified.
            scope: A JSON-serialized object, describing scope of users for which the commands are relevant. Defaults to BotCommandScopeDefault.
            language_code: A two-letter ISO 639-1 language code. If empty, commands will be applied to all users from the given scope, for whose language there are no dedicated commands.
        """
        return await self.call(SetMyCommands(
            commands=commands,
            scope=scope,
            language_code=language_code,
        ))

    async def delete_my_commands(
        self,
        *,
        scope: Optional[BotCommandScope] = None,
        language_code: Optional[str] = None,
    ) -> bool:
        """Use this method to delete the list of the bot's commands for the given scope and user language. After deletion, higher level commands will be shown to affected users. Returns True on success.
        
        https://core.telegram.org/bots/api#deletemycommands
        
        Args:
            scope: A JSON-serialized object, describing scope of users for which the commands are relevant. Defaults to BotCommandScopeDefault.
            language_code: A two-letter ISO 639-1 language code. If empty, commands will be applied to all users from the given scope, for whose language there are no dedicated commands.
        """
        return await self.call(DeleteMyCommands(
            scope=scope,
            language_code=language_code,
        ))

    async def get_my_commands(
        self,
        *,
        scope: Optional[BotCommandScope] = None,
        language_code: Optional[str] = None,
    ) -> List[BotCommand]:
        """Use this method to get the current list of the bot's commands for the given scope and user language. Returns an Array of BotCommand objects. If commands aren't set, an empty list is returned.
        
        https://core.telegram.org/bots/api#getmycommands
        
        Args:
            scope: A JSON-serialized object, describing scope of users. Defaults to BotCommandScopeDefault.
            language_code: A two-letter ISO 639-1 language code or an empty string
        """
        return await self.call(GetMyCommands(
            scope=scope,
            language_code=language_code,
        ))

    async def set_my_name(
        self,
        *,
        name: Optional[str] = None,
        language_code: Optional[str] = None,
    ) -> bool:
        """Use this method to change the bot's name. Returns True on success.
        
        https://core.telegram.org/bots/api#setmyname
        
        Args:
            name: New bot name; 0-64 characters. Pass an empty string to remove the dedicated name for the given language.
            language_code: A two-letter ISO 639-1 language code. If empty, the name will be shown to all users for whose language there is no dedicated name.
        """
        return await self.call(SetMyName(
            name=name,
            language_code=language_code,
        ))

    async def get_my_name(
        self,
        *,
        language_code: Optional[str] = None,
    ) -> BotName:
        """Use this method to get the current bot name for the given user language. Returns BotName on success.
        
        https://core.telegram.org/bots/api#getmyname
        
        Args:
            language_code: A two-letter ISO 639-1 language code or an empty string
        """
        return await self.call(GetMyName(
            language_code=language_code,
        ))

    async def set_my_description(
        self,
        *,
        description: Optional[str] = None,
        language_code: Optional[str] = None,
    ) -> bool:
        """Use this method to change the bot's description, which is shown in the chat with the bot if the chat is empty. Returns True on success.
        
        https://core.telegram.org/bots/api#setmydescription
        
        Args:
            description: New bot description; 0-512 characters. Pass an empty string to remove the dedicated description for the given language.
            language_code: A two-letter ISO 639-1 language code. If empty, the description will be applied to all users for whose language there is no dedicated description.
        """
        return await self.call(SetMyDescription(
            description=description,
            language_code=language_code,
        ))

    async def get_my_description(
        self,
        *,
        language_code: Optional[str] = None,
    ) -> BotDescription:
        """Use this method to get the current bot description for the given user language. Returns BotDescription on success.
        
        https://core.telegram.org/bots/api#getmydescription
        
        Args:
            language_code: A two-letter ISO 639-1 language code or an empty string
        """
        return await self.call(GetMyDescription(
            language_code=language_code,
        ))

    async def set_my_short_description(
        self,
        *,
        short_description: Optional[str] = None,
        language_code: Optional[str] = None,
    ) -> bool:
        """Use this method to change the bot's short description, which is shown on the bot's profile page and is sent together with the link when users share the bot. Returns True on success.
        
        https://core.telegram.org/bots/api#setmyshortdescription
        
        Args:
            short_description: New short description for the bot; 0-120 characters. Pass an empty string to remove the dedicated short description for the given language.
            language_code: A two-letter ISO 639-1 language code. If empty, the short description will be applied to all users for whose language there is no dedicated short description.
        """
        return await self.call(SetMyShortDescription(
            short_description=short_description,
            language_code=language_code,
        ))

    async def get_my_short_description(
        self,
        *,
        language_code: Optional[str] = None,
    ) -> BotShortDescription:
        """Use this method to get the current bot short description for the given user language. Returns BotShortDescription on success.
        
        https://core.telegram.org/bots/api#getmyshortdescription
        
        Args:
            language_code: A two-letter ISO 639-1 language code or an empty string
        """
        return await self.call(GetMyShortDescription(
            language_code=language_code,
        ))

    async def set_my_profile_photo(
        self,
        photo: InputProfilePhoto,
    ) -> bool:
        """Changes the profile photo of the bot. Returns True on success.
        
        https://core.telegram.org/bots/api#setmyprofilephoto
        
        Args:
            photo: The new profile photo to set
        """
        return await self.call(SetMyProfilePhoto(
            photo=photo,
        ))

    async def remove_my_profile_photo(
        self,
    ) -> bool:
        """Removes the profile photo of the bot. Requires no parameters. Returns True on success.
        
        https://core.telegram.org/bots/api#removemyprofilephoto
        """
        return await self.call(RemoveMyProfilePhoto(
        ))

    async def set_chat_menu_button(
        self,
        *,
        chat_id: Optional[int] = None,
        menu_button: Optional[MenuButton] = None,
    ) -> bool:
        """Use this method to change the bot's menu button in a private chat, or the default menu button. Returns True on success.
        
        https://core.telegram.org/bots/api#setchatmenubutton
        
        Args:
            chat_id: Unique identifier for the target private chat. If not specified, the bot's default menu button will be changed.
            menu_button: A JSON-serialized object for the bot's new menu button. Defaults to MenuButtonDefault.
        """
        return await self.call(SetChatMenuButton(
            chat_id=chat_id,
            menu_button=menu_button,
        ))

    async def get_chat_menu_button(
        self,
        *,
        chat_id: Optional[int] = None,
    ) -> MenuButton:
        """Use this method to get the current value of the bot's menu button in a private chat, or the default menu button. Returns MenuButton on success.
        
        https://core.telegram.org/bots/api#getchatmenubutton
        
        Args:
            chat_id: Unique identifier for the target private chat. If not specified, the bot's default menu button will be returned.
        """
        return await self.call(GetChatMenuButton(
            chat_id=chat_id,
        ))

    async def set_my_default_administrator_rights(
        self,
        *,
        rights: Optional[ChatAdministratorRights] = None,
        for_channels: Optional[bool] = None,
    ) -> bool:
        """Use this method to change the default administrator rights requested by the bot when it's added as an administrator to groups or channels. These rights will be suggested to users, but they are free to modify the list before adding the bot. Returns True on success.
        
        https://core.telegram.org/bots/api#setmydefaultadministratorrights
        
        Args:
            rights: A JSON-serialized object describing new default administrator rights. If not specified, the default administrator rights will be cleared.
            for_channels: Pass True to change the default administrator rights of the bot in channels. Otherwise, the default administrator rights of the bot for groups and supergroups will be changed.
        """
        return await self.call(SetMyDefaultAdministratorRights(
            rights=rights,
            for_channels=for_channels,
        ))

    async def get_my_default_administrator_rights(
        self,
        *,
        for_channels: Optional[bool] = None,
    ) -> ChatAdministratorRights:
        """Use this method to get the current default administrator rights of the bot. Returns ChatAdministratorRights on success.
        
        https://core.telegram.org/bots/api#getmydefaultadministratorrights
        
        Args:
            for_channels: Pass True to get default administrator rights of the bot in channels. Otherwise, default administrator rights of the bot for groups and supergroups will be returned.
        """
        return await self.call(GetMyDefaultAdministratorRights(
            for_channels=for_channels,
        ))

    async def get_available_gifts(
        self,
    ) -> Gifts:
        """Returns the list of gifts that can be sent by the bot to users and channel chats. Requires no parameters. Returns a Gifts object.
        
        https://core.telegram.org/bots/api#getavailablegifts
        """
        return await self.call(GetAvailableGifts(
        ))

    async def send_gift(
        self,
        gift_id: str,
        *,
        user_id: Optional[int] = None,
        chat_id: Optional[Union[int, str]] = None,
        pay_for_upgrade: Optional[bool] = None,
        text: Optional[str] = None,
        text_parse_mode: Optional[str] = None,
        text_entities: Optional[List[MessageEntity]] = None,
    ) -> bool:
        """Sends a gift to the given user or channel chat. The gift can't be converted to Telegram Stars by the receiver. Returns True on success.
        
        https://core.telegram.org/bots/api#sendgift
        
        Args:
            user_id: Required if chat_id is not specified. Unique identifier of the target user who will receive the gift.
            chat_id: Required if user_id is not specified. Unique identifier for the chat or username of the channel (in the format @username) that will receive the gift.
            gift_id: Identifier of the gift; limited gifts can't be sent to channel chats
            pay_for_upgrade: Pass True to pay for the gift upgrade from the bot's balance, thereby making the upgrade free for the receiver
            text: Text that will be shown along with the gift; 0-128 characters
            text_parse_mode: Mode for parsing entities in the text. See formatting options for more details. Entities other than "bold", "italic", "underline", "strikethrough", "spoiler", "custom_emoji", and "date_time" are ignored.
            text_entities: A JSON-serialized list of special entities that appear in the gift text. It can be specified instead of text_parse_mode. Entities other than "bold", "italic", "underline", "strikethrough", "spoiler", "custom_emoji", and "date_time" are ignored.
        """
        return await self.call(SendGift(
            user_id=user_id,
            chat_id=chat_id,
            gift_id=gift_id,
            pay_for_upgrade=pay_for_upgrade,
            text=text,
            text_parse_mode=text_parse_mode,
            text_entities=text_entities,
        ))

    async def gift_premium_subscription(
        self,
        user_id: int,
        month_count: int,
        star_count: int,
        *,
        text: Optional[str] = None,
        text_parse_mode: Optional[str] = None,
        text_entities: Optional[List[MessageEntity]] = None,
    ) -> bool:
        """Gifts a Telegram Premium subscription to the given user. Returns True on success.
        
        https://core.telegram.org/bots/api#giftpremiumsubscription
        
        Args:
            user_id: Unique identifier of the target user who will receive a Telegram Premium subscription
            month_count: Number of months the Telegram Premium subscription will be active for the user; must be one of 3, 6, or 12
            star_count: Number of Telegram Stars to pay for the Telegram Premium subscription; must be 1000 for 3 months, 1500 for 6 months, and 2500 for 12 months
            text: Text that will be shown along with the service message about the subscription; 0-128 characters
            text_parse_mode: Mode for parsing entities in the text. See formatting options for more details. Entities other than "bold", "italic", "underline", "strikethrough", "spoiler", "custom_emoji", and "date_time" are ignored.
            text_entities: A JSON-serialized list of special entities that appear in the gift text. It can be specified instead of text_parse_mode. Entities other than "bold", "italic", "underline", "strikethrough", "spoiler", "custom_emoji", and "date_time" are ignored.
        """
        return await self.call(GiftPremiumSubscription(
            user_id=user_id,
            month_count=month_count,
            star_count=star_count,
            text=text,
            text_parse_mode=text_parse_mode,
            text_entities=text_entities,
        ))

    async def verify_user(
        self,
        user_id: int,
        *,
        custom_description: Optional[str] = None,
    ) -> bool:
        """Verifies a user on behalf of the organization which is represented by the bot. Returns True on success.
        
        https://core.telegram.org/bots/api#verifyuser
        
        Args:
            user_id: Unique identifier of the target user
            custom_description: Custom description for the verification; 0-70 characters. Must be empty if the organization isn't allowed to provide a custom verification description.
        """
        return await self.call(VerifyUser(
            user_id=user_id,
            custom_description=custom_description,
        ))

    async def verify_chat(
        self,
        chat_id: Union[int, str],
        *,
        custom_description: Optional[str] = None,
    ) -> bool:
        """Verifies a chat on behalf of the organization which is represented by the bot. Returns True on success.
        
        https://core.telegram.org/bots/api#verifychat
        
        Args:
            chat_id: Unique identifier for the target chat or username of the target bot, supergroup or channel in the format @username. Channel direct messages chats can't be verified.
            custom_description: Custom description for the verification; 0-70 characters. Must be empty if the organization isn't allowed to provide a custom verification description.
        """
        return await self.call(VerifyChat(
            chat_id=chat_id,
            custom_description=custom_description,
        ))

    async def remove_user_verification(
        self,
        user_id: int,
    ) -> bool:
        """Removes verification from a user who is currently verified on behalf of the organization represented by the bot. Returns True on success.
        
        https://core.telegram.org/bots/api#removeuserverification
        
        Args:
            user_id: Unique identifier of the target user
        """
        return await self.call(RemoveUserVerification(
            user_id=user_id,
        ))

    async def remove_chat_verification(
        self,
        chat_id: Union[int, str],
    ) -> bool:
        """Removes verification from a chat that is currently verified on behalf of the organization represented by the bot. Returns True on success.
        
        https://core.telegram.org/bots/api#removechatverification
        
        Args:
            chat_id: Unique identifier for the target chat or username of the target bot or channel in the format @username
        """
        return await self.call(RemoveChatVerification(
            chat_id=chat_id,
        ))

    async def read_business_message(
        self,
        business_connection_id: str,
        chat_id: int,
        message_id: int,
    ) -> bool:
        """Marks incoming message as read on behalf of a business account. Requires the can_read_messages business bot right. Returns True on success.
        
        https://core.telegram.org/bots/api#readbusinessmessage
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which to read the message
            chat_id: Unique identifier of the chat in which the message was received. The chat must have been active in the last 24 hours.
            message_id: Unique identifier of the message to mark as read
        """
        return await self.call(ReadBusinessMessage(
            business_connection_id=business_connection_id,
            chat_id=chat_id,
            message_id=message_id,
        ))

    async def delete_business_messages(
        self,
        business_connection_id: str,
        message_ids: List[int],
    ) -> bool:
        """Delete messages on behalf of a business account. Requires the can_delete_sent_messages business bot right to delete messages sent by the bot itself, or the can_delete_all_messages business bot right to delete any message. Returns True on success.
        
        https://core.telegram.org/bots/api#deletebusinessmessages
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which to delete the messages
            message_ids: A JSON-serialized list of 1-100 identifiers of messages to delete. All messages must be from the same chat. See deleteMessage for limitations on which messages can be deleted.
        """
        return await self.call(DeleteBusinessMessages(
            business_connection_id=business_connection_id,
            message_ids=message_ids,
        ))

    async def set_business_account_name(
        self,
        business_connection_id: str,
        first_name: str,
        *,
        last_name: Optional[str] = None,
    ) -> bool:
        """Changes the first and last name of a managed business account. Requires the can_change_name business bot right. Returns True on success.
        
        https://core.telegram.org/bots/api#setbusinessaccountname
        
        Args:
            business_connection_id: Unique identifier of the business connection
            first_name: The new value of the first name for the business account; 1-64 characters
            last_name: The new value of the last name for the business account; 0-64 characters
        """
        return await self.call(SetBusinessAccountName(
            business_connection_id=business_connection_id,
            first_name=first_name,
            last_name=last_name,
        ))

    async def set_business_account_username(
        self,
        business_connection_id: str,
        *,
        username: Optional[str] = None,
    ) -> bool:
        """Changes the username of a managed business account. Requires the can_change_username business bot right. Returns True on success.
        
        https://core.telegram.org/bots/api#setbusinessaccountusername
        
        Args:
            business_connection_id: Unique identifier of the business connection
            username: The new value of the username for the business account; 0-32 characters
        """
        return await self.call(SetBusinessAccountUsername(
            business_connection_id=business_connection_id,
            username=username,
        ))

    async def set_business_account_bio(
        self,
        business_connection_id: str,
        *,
        bio: Optional[str] = None,
    ) -> bool:
        """Changes the bio of a managed business account. Requires the can_change_bio business bot right. Returns True on success.
        
        https://core.telegram.org/bots/api#setbusinessaccountbio
        
        Args:
            business_connection_id: Unique identifier of the business connection
            bio: The new value of the bio for the business account; 0-140 characters
        """
        return await self.call(SetBusinessAccountBio(
            business_connection_id=business_connection_id,
            bio=bio,
        ))

    async def set_business_account_profile_photo(
        self,
        business_connection_id: str,
        photo: InputProfilePhoto,
        *,
        is_public: Optional[bool] = None,
    ) -> bool:
        """Changes the profile photo of a managed business account. Requires the can_edit_profile_photo business bot right. Returns True on success.
        
        https://core.telegram.org/bots/api#setbusinessaccountprofilephoto
        
        Args:
            business_connection_id: Unique identifier of the business connection
            photo: The new profile photo to set
            is_public: Pass True to set the public photo, which will be visible even if the main photo is hidden by the business account's privacy settings. An account can have only one public photo.
        """
        return await self.call(SetBusinessAccountProfilePhoto(
            business_connection_id=business_connection_id,
            photo=photo,
            is_public=is_public,
        ))

    async def remove_business_account_profile_photo(
        self,
        business_connection_id: str,
        *,
        is_public: Optional[bool] = None,
    ) -> bool:
        """Removes the current profile photo of a managed business account. Requires the can_edit_profile_photo business bot right. Returns True on success.
        
        https://core.telegram.org/bots/api#removebusinessaccountprofilephoto
        
        Args:
            business_connection_id: Unique identifier of the business connection
            is_public: Pass True to remove the public photo, which is visible even if the main photo is hidden by the business account's privacy settings. After the main photo is removed, the previous profile photo (if present) becomes the main photo.
        """
        return await self.call(RemoveBusinessAccountProfilePhoto(
            business_connection_id=business_connection_id,
            is_public=is_public,
        ))

    async def set_business_account_gift_settings(
        self,
        business_connection_id: str,
        show_gift_button: bool,
        accepted_gift_types: AcceptedGiftTypes,
    ) -> bool:
        """Changes the privacy settings pertaining to incoming gifts in a managed business account. Requires the can_change_gift_settings business bot right. Returns True on success.
        
        https://core.telegram.org/bots/api#setbusinessaccountgiftsettings
        
        Args:
            business_connection_id: Unique identifier of the business connection
            show_gift_button: Pass True if a button for sending a gift to the user or by the business account must always be shown in the input field
            accepted_gift_types: Types of gifts accepted by the business account
        """
        return await self.call(SetBusinessAccountGiftSettings(
            business_connection_id=business_connection_id,
            show_gift_button=show_gift_button,
            accepted_gift_types=accepted_gift_types,
        ))

    async def get_business_account_star_balance(
        self,
        business_connection_id: str,
    ) -> StarAmount:
        """Returns the amount of Telegram Stars owned by a managed business account. Requires the can_view_gifts_and_stars business bot right. Returns StarAmount on success.
        
        https://core.telegram.org/bots/api#getbusinessaccountstarbalance
        
        Args:
            business_connection_id: Unique identifier of the business connection
        """
        return await self.call(GetBusinessAccountStarBalance(
            business_connection_id=business_connection_id,
        ))

    async def transfer_business_account_stars(
        self,
        business_connection_id: str,
        star_count: int,
    ) -> bool:
        """Transfers Telegram Stars from the business account balance to the bot's balance. Requires the can_transfer_stars business bot right. Returns True on success.
        
        https://core.telegram.org/bots/api#transferbusinessaccountstars
        
        Args:
            business_connection_id: Unique identifier of the business connection
            star_count: Number of Telegram Stars to transfer; 1-10000
        """
        return await self.call(TransferBusinessAccountStars(
            business_connection_id=business_connection_id,
            star_count=star_count,
        ))

    async def get_business_account_gifts(
        self,
        business_connection_id: str,
        *,
        exclude_unsaved: Optional[bool] = None,
        exclude_saved: Optional[bool] = None,
        exclude_unlimited: Optional[bool] = None,
        exclude_limited_upgradable: Optional[bool] = None,
        exclude_limited_non_upgradable: Optional[bool] = None,
        exclude_unique: Optional[bool] = None,
        exclude_from_blockchain: Optional[bool] = None,
        sort_by_price: Optional[bool] = None,
        offset: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> OwnedGifts:
        """Returns the gifts received and owned by a managed business account. Requires the can_view_gifts_and_stars business bot right. Returns OwnedGifts on success.
        
        https://core.telegram.org/bots/api#getbusinessaccountgifts
        
        Args:
            business_connection_id: Unique identifier of the business connection
            exclude_unsaved: Pass True to exclude gifts that aren't saved to the account's profile page
            exclude_saved: Pass True to exclude gifts that are saved to the account's profile page
            exclude_unlimited: Pass True to exclude gifts that can be purchased an unlimited number of times
            exclude_limited_upgradable: Pass True to exclude gifts that can be purchased a limited number of times and can be upgraded to unique
            exclude_limited_non_upgradable: Pass True to exclude gifts that can be purchased a limited number of times and can't be upgraded to unique
            exclude_unique: Pass True to exclude unique gifts
            exclude_from_blockchain: Pass True to exclude gifts that were assigned from the TON blockchain and can't be resold or transferred in Telegram
            sort_by_price: Pass True to sort results by gift price instead of send date. Sorting is applied before pagination.
            offset: Offset of the first entry to return as received from the previous request; use empty string to get the first chunk of results
            limit: The maximum number of gifts to be returned; 1-100. Defaults to 100.
        """
        return await self.call(GetBusinessAccountGifts(
            business_connection_id=business_connection_id,
            exclude_unsaved=exclude_unsaved,
            exclude_saved=exclude_saved,
            exclude_unlimited=exclude_unlimited,
            exclude_limited_upgradable=exclude_limited_upgradable,
            exclude_limited_non_upgradable=exclude_limited_non_upgradable,
            exclude_unique=exclude_unique,
            exclude_from_blockchain=exclude_from_blockchain,
            sort_by_price=sort_by_price,
            offset=offset,
            limit=limit,
        ))

    async def get_user_gifts(
        self,
        user_id: int,
        *,
        exclude_unlimited: Optional[bool] = None,
        exclude_limited_upgradable: Optional[bool] = None,
        exclude_limited_non_upgradable: Optional[bool] = None,
        exclude_from_blockchain: Optional[bool] = None,
        exclude_unique: Optional[bool] = None,
        sort_by_price: Optional[bool] = None,
        offset: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> OwnedGifts:
        """Returns the gifts owned and hosted by a user. Returns OwnedGifts on success.
        
        https://core.telegram.org/bots/api#getusergifts
        
        Args:
            user_id: Unique identifier of the user
            exclude_unlimited: Pass True to exclude gifts that can be purchased an unlimited number of times
            exclude_limited_upgradable: Pass True to exclude gifts that can be purchased a limited number of times and can be upgraded to unique
            exclude_limited_non_upgradable: Pass True to exclude gifts that can be purchased a limited number of times and can't be upgraded to unique
            exclude_from_blockchain: Pass True to exclude gifts that were assigned from the TON blockchain and can't be resold or transferred in Telegram
            exclude_unique: Pass True to exclude unique gifts
            sort_by_price: Pass True to sort results by gift price instead of send date. Sorting is applied before pagination.
            offset: Offset of the first entry to return as received from the previous request; use an empty string to get the first chunk of results
            limit: The maximum number of gifts to be returned; 1-100. Defaults to 100.
        """
        return await self.call(GetUserGifts(
            user_id=user_id,
            exclude_unlimited=exclude_unlimited,
            exclude_limited_upgradable=exclude_limited_upgradable,
            exclude_limited_non_upgradable=exclude_limited_non_upgradable,
            exclude_from_blockchain=exclude_from_blockchain,
            exclude_unique=exclude_unique,
            sort_by_price=sort_by_price,
            offset=offset,
            limit=limit,
        ))

    async def get_chat_gifts(
        self,
        chat_id: Union[int, str],
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
        """Returns the gifts owned by a chat. Returns OwnedGifts on success.
        
        https://core.telegram.org/bots/api#getchatgifts
        
        Args:
            chat_id: Unique identifier for the target chat or username of the target channel in the format @username
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
        return await self.call(GetChatGifts(
            chat_id=chat_id,
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
        ))

    async def convert_gift_to_stars(
        self,
        business_connection_id: str,
        owned_gift_id: str,
    ) -> bool:
        """Converts a given regular gift to Telegram Stars. Requires the can_convert_gifts_to_stars business bot right. Returns True on success.
        
        https://core.telegram.org/bots/api#convertgifttostars
        
        Args:
            business_connection_id: Unique identifier of the business connection
            owned_gift_id: Unique identifier of the regular gift that should be converted to Telegram Stars
        """
        return await self.call(ConvertGiftToStars(
            business_connection_id=business_connection_id,
            owned_gift_id=owned_gift_id,
        ))

    async def upgrade_gift(
        self,
        business_connection_id: str,
        owned_gift_id: str,
        *,
        keep_original_details: Optional[bool] = None,
        star_count: Optional[int] = None,
    ) -> bool:
        """Upgrades a given regular gift to a unique gift. Requires the can_transfer_and_upgrade_gifts business bot right. Additionally requires the can_transfer_stars business bot right if the upgrade is paid. Returns True on success.
        
        https://core.telegram.org/bots/api#upgradegift
        
        Args:
            business_connection_id: Unique identifier of the business connection
            owned_gift_id: Unique identifier of the regular gift that should be upgraded to a unique one
            keep_original_details: Pass True to keep the original gift text, sender and receiver in the upgraded gift
            star_count: The amount of Telegram Stars that will be paid for the upgrade from the business account balance. If gift.prepaid_upgrade_star_count > 0, then pass 0, otherwise, the can_transfer_stars business bot right is required and gift.upgrade_star_count must be passed.
        """
        return await self.call(UpgradeGift(
            business_connection_id=business_connection_id,
            owned_gift_id=owned_gift_id,
            keep_original_details=keep_original_details,
            star_count=star_count,
        ))

    async def transfer_gift(
        self,
        business_connection_id: str,
        owned_gift_id: str,
        new_owner_chat_id: int,
        *,
        star_count: Optional[int] = None,
    ) -> bool:
        """Transfers an owned unique gift to another user. Requires the can_transfer_and_upgrade_gifts business bot right. Requires can_transfer_stars business bot right if the transfer is paid. Returns True on success.
        
        https://core.telegram.org/bots/api#transfergift
        
        Args:
            business_connection_id: Unique identifier of the business connection
            owned_gift_id: Unique identifier of the regular gift that should be transferred
            new_owner_chat_id: Unique identifier of the chat which will own the gift. The chat must be active in the last 24 hours.
            star_count: The amount of Telegram Stars that will be paid for the transfer from the business account balance. If positive, then the can_transfer_stars business bot right is required.
        """
        return await self.call(TransferGift(
            business_connection_id=business_connection_id,
            owned_gift_id=owned_gift_id,
            new_owner_chat_id=new_owner_chat_id,
            star_count=star_count,
        ))

    async def post_story(
        self,
        business_connection_id: str,
        content: InputStoryContent,
        active_period: int,
        *,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        areas: Optional[List[StoryArea]] = None,
        post_to_chat_page: Optional[bool] = None,
        protect_content: Optional[bool] = None,
    ) -> Story:
        """Posts a story on behalf of a managed business account. Requires the can_manage_stories business bot right. Returns Story on success.
        
        https://core.telegram.org/bots/api#poststory
        
        Args:
            business_connection_id: Unique identifier of the business connection
            content: Content of the story
            active_period: Period after which the story is moved to the archive, in seconds; must be one of 6 * 3600, 12 * 3600, 86400, or 2 * 86400
            caption: Caption of the story, 0-2048 characters after entities parsing
            parse_mode: Mode for parsing entities in the story caption. See formatting options for more details.
            caption_entities: A JSON-serialized list of special entities that appear in the caption, which can be specified instead of parse_mode
            areas: A JSON-serialized list of clickable areas to be shown on the story
            post_to_chat_page: Pass True to keep the story accessible after it expires
            protect_content: Pass True if the content of the story must be protected from forwarding and screenshotting
        """
        return await self.call(PostStory(
            business_connection_id=business_connection_id,
            content=content,
            active_period=active_period,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            areas=areas,
            post_to_chat_page=post_to_chat_page,
            protect_content=protect_content,
        ))

    async def repost_story(
        self,
        business_connection_id: str,
        from_chat_id: int,
        from_story_id: int,
        active_period: int,
        *,
        post_to_chat_page: Optional[bool] = None,
        protect_content: Optional[bool] = None,
    ) -> Story:
        """Reposts a story on behalf of a business account from another business account. Both business accounts must be managed by the same bot, and the story on the source account must have been posted (or reposted) by the bot. Requires the can_manage_stories business bot right for both business accounts. Returns Story on success.
        
        https://core.telegram.org/bots/api#repoststory
        
        Args:
            business_connection_id: Unique identifier of the business connection
            from_chat_id: Unique identifier of the chat which posted the story that should be reposted
            from_story_id: Unique identifier of the story that should be reposted
            active_period: Period after which the story is moved to the archive, in seconds; must be one of 6 * 3600, 12 * 3600, 86400, or 2 * 86400
            post_to_chat_page: Pass True to keep the story accessible after it expires
            protect_content: Pass True if the content of the story must be protected from forwarding and screenshotting
        """
        return await self.call(RepostStory(
            business_connection_id=business_connection_id,
            from_chat_id=from_chat_id,
            from_story_id=from_story_id,
            active_period=active_period,
            post_to_chat_page=post_to_chat_page,
            protect_content=protect_content,
        ))

    async def edit_story(
        self,
        business_connection_id: str,
        story_id: int,
        content: InputStoryContent,
        *,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        areas: Optional[List[StoryArea]] = None,
    ) -> Story:
        """Edits a story previously posted by the bot on behalf of a managed business account. Requires the can_manage_stories business bot right. Returns Story on success.
        
        https://core.telegram.org/bots/api#editstory
        
        Args:
            business_connection_id: Unique identifier of the business connection
            story_id: Unique identifier of the story to edit
            content: Content of the story
            caption: Caption of the story, 0-2048 characters after entities parsing
            parse_mode: Mode for parsing entities in the story caption. See formatting options for more details.
            caption_entities: A JSON-serialized list of special entities that appear in the caption, which can be specified instead of parse_mode
            areas: A JSON-serialized list of clickable areas to be shown on the story
        """
        return await self.call(EditStory(
            business_connection_id=business_connection_id,
            story_id=story_id,
            content=content,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            areas=areas,
        ))

    async def delete_story(
        self,
        business_connection_id: str,
        story_id: int,
    ) -> bool:
        """Deletes a story previously posted by the bot on behalf of a managed business account. Requires the can_manage_stories business bot right. Returns True on success.
        
        https://core.telegram.org/bots/api#deletestory
        
        Args:
            business_connection_id: Unique identifier of the business connection
            story_id: Unique identifier of the story to delete
        """
        return await self.call(DeleteStory(
            business_connection_id=business_connection_id,
            story_id=story_id,
        ))

    async def answer_web_app_query(
        self,
        web_app_query_id: str,
        result: InlineQueryResult,
    ) -> SentWebAppMessage:
        """Use this method to set the result of an interaction with a Web App and send a corresponding message on behalf of the user to the chat from which the query originated. On success, a SentWebAppMessage object is returned.
        
        https://core.telegram.org/bots/api#answerwebappquery
        
        Args:
            web_app_query_id: Unique identifier for the query to be answered
            result: A JSON-serialized object describing the message to be sent
        """
        return await self.call(AnswerWebAppQuery(
            web_app_query_id=web_app_query_id,
            result=result,
        ))

    async def save_prepared_inline_message(
        self,
        user_id: int,
        result: InlineQueryResult,
        *,
        allow_user_chats: Optional[bool] = None,
        allow_bot_chats: Optional[bool] = None,
        allow_group_chats: Optional[bool] = None,
        allow_channel_chats: Optional[bool] = None,
    ) -> PreparedInlineMessage:
        """Stores a message that can be sent by a user of a Mini App. Returns a PreparedInlineMessage object.
        
        https://core.telegram.org/bots/api#savepreparedinlinemessage
        
        Args:
            user_id: Unique identifier of the target user that can use the prepared message
            result: A JSON-serialized object describing the message to be sent
            allow_user_chats: Pass True if the message can be sent to private chats with users
            allow_bot_chats: Pass True if the message can be sent to private chats with bots
            allow_group_chats: Pass True if the message can be sent to group and supergroup chats
            allow_channel_chats: Pass True if the message can be sent to channel chats
        """
        return await self.call(SavePreparedInlineMessage(
            user_id=user_id,
            result=result,
            allow_user_chats=allow_user_chats,
            allow_bot_chats=allow_bot_chats,
            allow_group_chats=allow_group_chats,
            allow_channel_chats=allow_channel_chats,
        ))

    async def save_prepared_keyboard_button(
        self,
        user_id: int,
        button: KeyboardButton,
    ) -> PreparedKeyboardButton:
        """Stores a keyboard button that can be used by a user within a Mini App. Returns a PreparedKeyboardButton object.
        
        https://core.telegram.org/bots/api#savepreparedkeyboardbutton
        
        Args:
            user_id: Unique identifier of the target user that can use the button
            button: A JSON-serialized object describing the button to be saved. The button must be of the type request_users, request_chat, or request_managed_bot.
        """
        return await self.call(SavePreparedKeyboardButton(
            user_id=user_id,
            button=button,
        ))

    async def edit_message_text(
        self,
        *,
        business_connection_id: Optional[str] = None,
        chat_id: Optional[Union[int, str]] = None,
        message_id: Optional[int] = None,
        inline_message_id: Optional[str] = None,
        text: Optional[str] = None,
        parse_mode: Optional[str] = None,
        entities: Optional[List[MessageEntity]] = None,
        link_preview_options: Optional[LinkPreviewOptions] = None,
        rich_message: Optional[InputRichMessage] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ) -> Union[Message, bool]:
        """Use this method to edit text, rich and game messages. On success, if the edited message is not an inline message, the edited Message is returned, otherwise True is returned. Note that business messages that were not sent by the bot and do not contain an inline keyboard can only be edited within 48 hours from the time they were sent.
        
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
        return await self.call(EditMessageText(
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
        ))

    async def edit_message_caption(
        self,
        *,
        business_connection_id: Optional[str] = None,
        chat_id: Optional[Union[int, str]] = None,
        message_id: Optional[int] = None,
        inline_message_id: Optional[str] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        show_caption_above_media: Optional[bool] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ) -> Union[Message, bool]:
        """Use this method to edit captions of messages. On success, if the edited message is not an inline message, the edited Message is returned, otherwise True is returned. Note that business messages that were not sent by the bot and do not contain an inline keyboard can only be edited within 48 hours from the time they were sent.
        
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
        return await self.call(EditMessageCaption(
            business_connection_id=business_connection_id,
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            show_caption_above_media=show_caption_above_media,
            reply_markup=reply_markup,
        ))

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
        """Use this method to edit animation, audio, document, live photo, photo, or video messages, or to replace a text or a rich message with a media. If a message is part of a message album, then it can be edited only to an audio for audio albums, only to a document for document albums and to a photo, a live photo, or a video otherwise. When an inline message is edited, a new file can't be uploaded; use a previously uploaded file via its file_id or specify a URL. On success, if the edited message is not an inline message, the edited Message is returned, otherwise True is returned. Note that business messages that were not sent by the bot and do not contain an inline keyboard can only be edited within 48 hours from the time they were sent.
        
        https://core.telegram.org/bots/api#editmessagemedia
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message to be edited was sent
            chat_id: Required if inline_message_id is not specified. Unique identifier for the target chat or username of the target bot, supergroup or channel in the format @username.
            message_id: Required if inline_message_id is not specified. Identifier of the message to edit.
            inline_message_id: Required if chat_id and message_id are not specified. Identifier of the inline message.
            media: A JSON-serialized object for the new media content of the message
            reply_markup: A JSON-serialized object for a new inline keyboard
        """
        return await self.call(EditMessageMedia(
            business_connection_id=business_connection_id,
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
            media=media,
            reply_markup=reply_markup,
        ))

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
        """Use this method to edit live location messages. A location can be edited until its live_period expires or editing is explicitly disabled by a call to stopMessageLiveLocation. On success, if the edited message is not an inline message, the edited Message is returned, otherwise True is returned.
        
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
        return await self.call(EditMessageLiveLocation(
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
        ))

    async def stop_message_live_location(
        self,
        *,
        business_connection_id: Optional[str] = None,
        chat_id: Optional[Union[int, str]] = None,
        message_id: Optional[int] = None,
        inline_message_id: Optional[str] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ) -> Union[Message, bool]:
        """Use this method to stop updating a live location message before live_period expires. On success, if the message is not an inline message, the edited Message is returned, otherwise True is returned.
        
        https://core.telegram.org/bots/api#stopmessagelivelocation
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message to be edited was sent
            chat_id: Required if inline_message_id is not specified. Unique identifier for the target chat or username of the target bot, supergroup or channel in the format @username.
            message_id: Required if inline_message_id is not specified. Identifier of the message with live location to stop.
            inline_message_id: Required if chat_id and message_id are not specified. Identifier of the inline message.
            reply_markup: A JSON-serialized object for a new inline keyboard
        """
        return await self.call(StopMessageLiveLocation(
            business_connection_id=business_connection_id,
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
            reply_markup=reply_markup,
        ))

    async def edit_message_checklist(
        self,
        business_connection_id: str,
        chat_id: Union[int, str],
        message_id: int,
        checklist: InputChecklist,
        *,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ) -> Message:
        """Use this method to edit a checklist on behalf of a connected business account. On success, the edited Message is returned.
        
        https://core.telegram.org/bots/api#editmessagechecklist
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
            chat_id: Unique identifier for the target chat or username of the target bot in the format @username
            message_id: Unique identifier for the target message
            checklist: A JSON-serialized object for the new checklist
            reply_markup: A JSON-serialized object for the new inline keyboard for the message
        """
        return await self.call(EditMessageChecklist(
            business_connection_id=business_connection_id,
            chat_id=chat_id,
            message_id=message_id,
            checklist=checklist,
            reply_markup=reply_markup,
        ))

    async def edit_message_reply_markup(
        self,
        *,
        business_connection_id: Optional[str] = None,
        chat_id: Optional[Union[int, str]] = None,
        message_id: Optional[int] = None,
        inline_message_id: Optional[str] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ) -> Union[Message, bool]:
        """Use this method to edit only the reply markup of messages. On success, if the edited message is not an inline message, the edited Message is returned, otherwise True is returned. Note that business messages that were not sent by the bot and do not contain an inline keyboard can only be edited within 48 hours from the time they were sent.
        
        https://core.telegram.org/bots/api#editmessagereplymarkup
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message to be edited was sent
            chat_id: Required if inline_message_id is not specified. Unique identifier for the target chat or username of the target bot, supergroup or channel in the format @username.
            message_id: Required if inline_message_id is not specified. Identifier of the message to edit.
            inline_message_id: Required if chat_id and message_id are not specified. Identifier of the inline message.
            reply_markup: A JSON-serialized object for an inline keyboard
        """
        return await self.call(EditMessageReplyMarkup(
            business_connection_id=business_connection_id,
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
            reply_markup=reply_markup,
        ))

    async def stop_poll(
        self,
        chat_id: Union[int, str],
        message_id: int,
        *,
        business_connection_id: Optional[str] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ) -> Poll:
        """Use this method to stop a poll which was sent by the bot. On success, the stopped Poll is returned.
        
        https://core.telegram.org/bots/api#stoppoll
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message to be edited was sent
            chat_id: Unique identifier for the target chat or username of the target bot, supergroup or channel in the format @username
            message_id: Identifier of the original message with the poll
            reply_markup: A JSON-serialized object for a new message inline keyboard
        """
        return await self.call(StopPoll(
            business_connection_id=business_connection_id,
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=reply_markup,
        ))

    async def edit_ephemeral_message_text(
        self,
        chat_id: Union[int, str],
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
        """Use this method to edit an ephemeral text or rich message. Note that it is not guaranteed that the user will receive the message edit event, especially if they are offline. On success, True is returned.
        
        https://core.telegram.org/bots/api#editephemeralmessagetext
        
        Args:
            chat_id: Unique identifier for the target chat or username of the target supergroup in the format @username
            receiver_user_id: Identifier of the user who received the message
            ephemeral_message_id: Identifier of the ephemeral message to edit
            text: New text of the message, 1-4096 characters after entity parsing; required if rich_message isn't specified
            parse_mode: Mode for parsing entities in the message text. See formatting options for more details.
            entities: A JSON-serialized list of special entities that appear in message text, which can be specified instead of parse_mode
            rich_message: New rich content of the message; required if text isn't specified
            link_preview_options: Link preview generation options for the message
            reply_markup: A JSON-serialized object for an inline keyboard
        """
        return await self.call(EditEphemeralMessageText(
            chat_id=chat_id,
            receiver_user_id=receiver_user_id,
            ephemeral_message_id=ephemeral_message_id,
            text=text,
            parse_mode=parse_mode,
            entities=entities,
            rich_message=rich_message,
            link_preview_options=link_preview_options,
            reply_markup=reply_markup,
        ))

    async def edit_ephemeral_message_media(
        self,
        chat_id: Union[int, str],
        receiver_user_id: int,
        ephemeral_message_id: int,
        media: InputMedia,
        *,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ) -> bool:
        """Use this method to edit the media of an ephemeral message. Note that it is not guaranteed that the user will receive the message edit event, especially if they are offline. On success, True is returned.
        
        https://core.telegram.org/bots/api#editephemeralmessagemedia
        
        Args:
            chat_id: Unique identifier for the target chat or username of the target supergroup in the format @username
            receiver_user_id: Identifier of the user who received the message
            ephemeral_message_id: Identifier of the ephemeral message to edit
            media: A JSON-serialized object for the new media content of the message
            reply_markup: A JSON-serialized object for an inline keyboard
        """
        return await self.call(EditEphemeralMessageMedia(
            chat_id=chat_id,
            receiver_user_id=receiver_user_id,
            ephemeral_message_id=ephemeral_message_id,
            media=media,
            reply_markup=reply_markup,
        ))

    async def edit_ephemeral_message_caption(
        self,
        chat_id: Union[int, str],
        receiver_user_id: int,
        ephemeral_message_id: int,
        *,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        show_caption_above_media: Optional[bool] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ) -> bool:
        """Use this method to edit the caption of an ephemeral message. Note that it is not guaranteed that the user will receive the message edit event, especially if they are offline. On success, True is returned.
        
        https://core.telegram.org/bots/api#editephemeralmessagecaption
        
        Args:
            chat_id: Unique identifier for the target chat or username of the target supergroup in the format @username
            receiver_user_id: Identifier of the user who received the message
            ephemeral_message_id: Identifier of the ephemeral message to edit
            caption: New caption of the message, 0-1024 characters after entities parsing
            parse_mode: Mode for parsing entities in the message caption. See formatting options for more details.
            caption_entities: A JSON-serialized list of special entities that appear in the caption, which can be specified instead of parse_mode
            show_caption_above_media: Pass True if the caption must be shown above the message media. Supported only for animation, photo and video messages.
            reply_markup: A JSON-serialized object for an inline keyboard
        """
        return await self.call(EditEphemeralMessageCaption(
            chat_id=chat_id,
            receiver_user_id=receiver_user_id,
            ephemeral_message_id=ephemeral_message_id,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            show_caption_above_media=show_caption_above_media,
            reply_markup=reply_markup,
        ))

    async def edit_ephemeral_message_reply_markup(
        self,
        chat_id: Union[int, str],
        receiver_user_id: int,
        ephemeral_message_id: int,
        *,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ) -> bool:
        """Use this method to edit only the reply markup of an ephemeral message. Note that it is not guaranteed that the user will receive the message edit event, especially if they are offline. On success, True is returned.
        
        https://core.telegram.org/bots/api#editephemeralmessagereplymarkup
        
        Args:
            chat_id: Unique identifier for the target chat or username of the target supergroup in the format @username
            receiver_user_id: Identifier of the user who received the message
            ephemeral_message_id: Identifier of the ephemeral message to edit
            reply_markup: A JSON-serialized object for an inline keyboard
        """
        return await self.call(EditEphemeralMessageReplyMarkup(
            chat_id=chat_id,
            receiver_user_id=receiver_user_id,
            ephemeral_message_id=ephemeral_message_id,
            reply_markup=reply_markup,
        ))

    async def approve_suggested_post(
        self,
        chat_id: int,
        message_id: int,
        *,
        send_date: Optional[int] = None,
    ) -> bool:
        """Use this method to approve a suggested post in a direct messages chat. The bot must have the 'can_post_messages' administrator right in the corresponding channel chat. Returns True on success.
        
        https://core.telegram.org/bots/api#approvesuggestedpost
        
        Args:
            chat_id: Unique identifier for the target direct messages chat
            message_id: Identifier of a suggested post message to approve
            send_date: Point in time (Unix timestamp) when the post is expected to be published; omit if the date has already been specified when the suggested post was created. If specified, then the date must be not more than 2678400 seconds (30 days) in the future.
        """
        return await self.call(ApproveSuggestedPost(
            chat_id=chat_id,
            message_id=message_id,
            send_date=send_date,
        ))

    async def decline_suggested_post(
        self,
        chat_id: int,
        message_id: int,
        *,
        comment: Optional[str] = None,
    ) -> bool:
        """Use this method to decline a suggested post in a direct messages chat. The bot must have the 'can_manage_direct_messages' administrator right in the corresponding channel chat. Returns True on success.
        
        https://core.telegram.org/bots/api#declinesuggestedpost
        
        Args:
            chat_id: Unique identifier for the target direct messages chat
            message_id: Identifier of a suggested post message to decline
            comment: Comment for the creator of the suggested post; 0-128 characters
        """
        return await self.call(DeclineSuggestedPost(
            chat_id=chat_id,
            message_id=message_id,
            comment=comment,
        ))

    async def delete_message(
        self,
        chat_id: Union[int, str],
        message_id: int,
    ) -> bool:
        """Use this method to delete a message, including service messages, with the following limitations:
        
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
            chat_id: Unique identifier for the target chat or username of the target bot, supergroup or channel in the format @username
            message_id: Identifier of the message to delete
        """
        return await self.call(DeleteMessage(
            chat_id=chat_id,
            message_id=message_id,
        ))

    async def delete_messages(
        self,
        chat_id: Union[int, str],
        message_ids: List[int],
    ) -> bool:
        """Use this method to delete multiple messages simultaneously. If some of the specified messages can't be found, they are skipped. Returns True on success.
        
        https://core.telegram.org/bots/api#deletemessages
        
        Args:
            chat_id: Unique identifier for the target chat or username of the target bot, supergroup or channel in the format @username
            message_ids: A JSON-serialized list of 1-100 identifiers of messages to delete. See deleteMessage for limitations on which messages can be deleted.
        """
        return await self.call(DeleteMessages(
            chat_id=chat_id,
            message_ids=message_ids,
        ))

    async def delete_ephemeral_message(
        self,
        chat_id: Union[int, str],
        receiver_user_id: int,
        ephemeral_message_id: int,
    ) -> bool:
        """Use this method to delete an ephemeral message. Note that it is not guaranteed that the user will receive the message deletion event, especially if they are offline. Returns True on success.
        
        https://core.telegram.org/bots/api#deleteephemeralmessage
        
        Args:
            chat_id: Unique identifier for the target chat or username of the target supergroup in the format @username
            receiver_user_id: Identifier of the user who received the message
            ephemeral_message_id: Identifier of the ephemeral message to delete
        """
        return await self.call(DeleteEphemeralMessage(
            chat_id=chat_id,
            receiver_user_id=receiver_user_id,
            ephemeral_message_id=ephemeral_message_id,
        ))

    async def delete_message_reaction(
        self,
        chat_id: Union[int, str],
        message_id: int,
        *,
        user_id: Optional[int] = None,
        actor_chat_id: Optional[int] = None,
    ) -> bool:
        """Use this method to remove a reaction from a message in a group or a supergroup chat. The bot must have the 'can_delete_messages' administrator right in the chat. Returns True on success.
        
        https://core.telegram.org/bots/api#deletemessagereaction
        
        Args:
            chat_id: Unique identifier for the target chat or username of the target supergroup in the format @username
            message_id: Identifier of the target message
            user_id: Identifier of the user whose reaction will be removed, if the reaction was added by a user
            actor_chat_id: Identifier of the chat whose reaction will be removed, if the reaction was added by a chat
        """
        return await self.call(DeleteMessageReaction(
            chat_id=chat_id,
            message_id=message_id,
            user_id=user_id,
            actor_chat_id=actor_chat_id,
        ))

    async def delete_all_message_reactions(
        self,
        chat_id: Union[int, str],
        *,
        user_id: Optional[int] = None,
        actor_chat_id: Optional[int] = None,
    ) -> bool:
        """Use this method to remove up to 10000 recent reactions in a group or a supergroup chat added by a given user or chat. The bot must have the 'can_delete_messages' administrator right in the chat. Returns True on success.
        
        https://core.telegram.org/bots/api#deleteallmessagereactions
        
        Args:
            chat_id: Unique identifier for the target chat or username of the target supergroup in the format @username
            user_id: Identifier of the user whose reactions will be removed, if the reactions were added by a user
            actor_chat_id: Identifier of the chat whose reactions will be removed, if the reactions were added by a chat
        """
        return await self.call(DeleteAllMessageReactions(
            chat_id=chat_id,
            user_id=user_id,
            actor_chat_id=actor_chat_id,
        ))

    async def send_sticker(
        self,
        chat_id: Union[int, str],
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
        """Use this method to send static .WEBP, animated .TGS, or video .WEBM stickers. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendsticker
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
            chat_id: Unique identifier for the target chat or username of the target bot, supergroup or channel in the format @username
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
        return await self.call(SendSticker(
            business_connection_id=business_connection_id,
            chat_id=chat_id,
            message_thread_id=message_thread_id,
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
        ))

    async def get_sticker_set(
        self,
        name: str,
    ) -> StickerSet:
        """Use this method to get a sticker set. On success, a StickerSet object is returned.
        
        https://core.telegram.org/bots/api#getstickerset
        
        Args:
            name: Name of the sticker set
        """
        return await self.call(GetStickerSet(
            name=name,
        ))

    async def get_custom_emoji_stickers(
        self,
        custom_emoji_ids: List[str],
    ) -> List[Sticker]:
        """Use this method to get information about custom emoji stickers by their identifiers. Returns an Array of Sticker objects.
        
        https://core.telegram.org/bots/api#getcustomemojistickers
        
        Args:
            custom_emoji_ids: A JSON-serialized list of custom emoji identifiers. At most 200 custom emoji identifiers can be specified.
        """
        return await self.call(GetCustomEmojiStickers(
            custom_emoji_ids=custom_emoji_ids,
        ))

    async def upload_sticker_file(
        self,
        user_id: int,
        sticker: InputFile,
        sticker_format: str,
    ) -> File:
        """Use this method to upload a file with a sticker for later use in the createNewStickerSet, addStickerToSet, or replaceStickerInSet methods (the file can be used multiple times). Returns the uploaded File on success.
        
        https://core.telegram.org/bots/api#uploadstickerfile
        
        Args:
            user_id: User identifier of sticker file owner
            sticker: A file with the sticker in .WEBP, .PNG, .TGS, or .WEBM format. See https://core.telegram.org/stickers for technical requirements. More information on Sending Files: https://core.telegram.org/bots/api#sending-files
            sticker_format: Format of the sticker, must be one of "static", "animated", "video" 
        """
        return await self.call(UploadStickerFile(
            user_id=user_id,
            sticker=sticker,
            sticker_format=sticker_format,
        ))

    async def create_new_sticker_set(
        self,
        user_id: int,
        name: str,
        title: str,
        stickers: List[InputSticker],
        *,
        sticker_type: Optional[str] = None,
        needs_repainting: Optional[bool] = None,
    ) -> bool:
        """Use this method to create a new sticker set owned by a user. The bot will be able to edit the sticker set thus created. Returns True on success.
        
        https://core.telegram.org/bots/api#createnewstickerset
        
        Args:
            user_id: User identifier of created sticker set owner
            name: Short name of sticker set, to be used in t.me/addstickers/ URLs (e.g., animals). Can contain only English letters, digits and underscores. Must begin with a letter, can't contain consecutive underscores and must end in "_by_<bot_username>". <bot_username> is case insensitive. 1-64 characters.
            title: Sticker set title, 1-64 characters
            stickers: A JSON-serialized list of 1-50 initial stickers to be added to the sticker set
            sticker_type: Type of stickers in the set, pass "regular", "mask", or "custom_emoji". By default, a regular sticker set is created.
            needs_repainting: Pass True if stickers in the sticker set must be repainted to the color of text when used in messages, the accent color if used as emoji status, white on chat photos, or another appropriate color based on context; for custom emoji sticker sets only
        """
        return await self.call(CreateNewStickerSet(
            user_id=user_id,
            name=name,
            title=title,
            stickers=stickers,
            sticker_type=sticker_type,
            needs_repainting=needs_repainting,
        ))

    async def add_sticker_to_set(
        self,
        user_id: int,
        name: str,
        sticker: InputSticker,
    ) -> bool:
        """Use this method to add a new sticker to a set created by the bot. Emoji sticker sets can have up to 200 stickers. Other sticker sets can have up to 120 stickers. Returns True on success.
        
        https://core.telegram.org/bots/api#addstickertoset
        
        Args:
            user_id: User identifier of sticker set owner
            name: Sticker set name
            sticker: A JSON-serialized object with information about the added sticker. If exactly the same sticker had already been added to the set, then the set isn't changed.
        """
        return await self.call(AddStickerToSet(
            user_id=user_id,
            name=name,
            sticker=sticker,
        ))

    async def set_sticker_position_in_set(
        self,
        sticker: str,
        position: int,
    ) -> bool:
        """Use this method to move a sticker in a set created by the bot to a specific position. Returns True on success.
        
        https://core.telegram.org/bots/api#setstickerpositioninset
        
        Args:
            sticker: File identifier of the sticker
            position: New sticker position in the set, zero-based
        """
        return await self.call(SetStickerPositionInSet(
            sticker=sticker,
            position=position,
        ))

    async def delete_sticker_from_set(
        self,
        sticker: str,
    ) -> bool:
        """Use this method to delete a sticker from a set created by the bot. Returns True on success.
        
        https://core.telegram.org/bots/api#deletestickerfromset
        
        Args:
            sticker: File identifier of the sticker
        """
        return await self.call(DeleteStickerFromSet(
            sticker=sticker,
        ))

    async def replace_sticker_in_set(
        self,
        user_id: int,
        name: str,
        old_sticker: str,
        sticker: InputSticker,
    ) -> bool:
        """Use this method to replace an existing sticker in a sticker set with a new one. The method is equivalent to calling deleteStickerFromSet, then addStickerToSet, then setStickerPositionInSet. Returns True on success.
        
        https://core.telegram.org/bots/api#replacestickerinset
        
        Args:
            user_id: User identifier of the sticker set owner
            name: Sticker set name
            old_sticker: File identifier of the replaced sticker
            sticker: A JSON-serialized object with information about the added sticker. If exactly the same sticker had already been added to the set, then the set remains unchanged.
        """
        return await self.call(ReplaceStickerInSet(
            user_id=user_id,
            name=name,
            old_sticker=old_sticker,
            sticker=sticker,
        ))

    async def set_sticker_emoji_list(
        self,
        sticker: str,
        emoji_list: List[str],
    ) -> bool:
        """Use this method to change the list of emoji assigned to a regular or custom emoji sticker. The sticker must belong to a sticker set created by the bot. Returns True on success.
        
        https://core.telegram.org/bots/api#setstickeremojilist
        
        Args:
            sticker: File identifier of the sticker
            emoji_list: A JSON-serialized list of 1-20 emoji associated with the sticker
        """
        return await self.call(SetStickerEmojiList(
            sticker=sticker,
            emoji_list=emoji_list,
        ))

    async def set_sticker_keywords(
        self,
        sticker: str,
        *,
        keywords: Optional[List[str]] = None,
    ) -> bool:
        """Use this method to change search keywords assigned to a regular or custom emoji sticker. The sticker must belong to a sticker set created by the bot. Returns True on success.
        
        https://core.telegram.org/bots/api#setstickerkeywords
        
        Args:
            sticker: File identifier of the sticker
            keywords: A JSON-serialized list of 0-20 search keywords for the sticker with total length of up to 64 characters
        """
        return await self.call(SetStickerKeywords(
            sticker=sticker,
            keywords=keywords,
        ))

    async def set_sticker_mask_position(
        self,
        sticker: str,
        *,
        mask_position: Optional[MaskPosition] = None,
    ) -> bool:
        """Use this method to change the mask position of a mask sticker. The sticker must belong to a sticker set that was created by the bot. Returns True on success.
        
        https://core.telegram.org/bots/api#setstickermaskposition
        
        Args:
            sticker: File identifier of the sticker
            mask_position: A JSON-serialized object with the position where the mask should be placed on faces. Omit the parameter to remove the mask position.
        """
        return await self.call(SetStickerMaskPosition(
            sticker=sticker,
            mask_position=mask_position,
        ))

    async def set_sticker_set_title(
        self,
        name: str,
        title: str,
    ) -> bool:
        """Use this method to set the title of a created sticker set. Returns True on success.
        
        https://core.telegram.org/bots/api#setstickersettitle
        
        Args:
            name: Sticker set name
            title: Sticker set title, 1-64 characters
        """
        return await self.call(SetStickerSetTitle(
            name=name,
            title=title,
        ))

    async def set_sticker_set_thumbnail(
        self,
        name: str,
        user_id: int,
        format: str,
        *,
        thumbnail: Optional[Union[InputFile, str]] = None,
    ) -> bool:
        """Use this method to set the thumbnail of a regular or mask sticker set. The format of the thumbnail file must match the format of the stickers in the set. Returns True on success.
        
        https://core.telegram.org/bots/api#setstickersetthumbnail
        
        Args:
            name: Sticker set name
            user_id: User identifier of the sticker set owner
            thumbnail: A .WEBP or .PNG image with the thumbnail, must be up to 128 kilobytes in size and have a width and height of exactly 100px, or a .TGS animation with a thumbnail up to 32 kilobytes in size (see https://core.telegram.org/stickers#animation-requirements for animated sticker technical requirements), or a .WEBM video with the thumbnail up to 32 kilobytes in size; see https://core.telegram.org/stickers#video-requirements for video sticker technical requirements. Pass a file_id as a String to send a file that already exists on the Telegram servers, pass an HTTP URL as a String for Telegram to get a file from the Internet, or upload a new one using multipart/form-data. More information on Sending Files: https://core.telegram.org/bots/api#sending-files. Animated and video sticker set thumbnails can't be uploaded via HTTP URL. If omitted, then the thumbnail is dropped and the first sticker is used as the thumbnail.
            format: Format of the thumbnail, must be one of "static" for a .WEBP or .PNG image, "animated" for a .TGS animation, or "video" for a .WEBM video
        """
        return await self.call(SetStickerSetThumbnail(
            name=name,
            user_id=user_id,
            thumbnail=thumbnail,
            format=format,
        ))

    async def set_custom_emoji_sticker_set_thumbnail(
        self,
        name: str,
        *,
        custom_emoji_id: Optional[str] = None,
    ) -> bool:
        """Use this method to set the thumbnail of a custom emoji sticker set. Returns True on success.
        
        https://core.telegram.org/bots/api#setcustomemojistickersetthumbnail
        
        Args:
            name: Sticker set name
            custom_emoji_id: Custom emoji identifier of a sticker from the sticker set; pass an empty string to drop the thumbnail and use the first sticker as the thumbnail
        """
        return await self.call(SetCustomEmojiStickerSetThumbnail(
            name=name,
            custom_emoji_id=custom_emoji_id,
        ))

    async def delete_sticker_set(
        self,
        name: str,
    ) -> bool:
        """Use this method to delete a sticker set that was created by the bot. Returns True on success.
        
        https://core.telegram.org/bots/api#deletestickerset
        
        Args:
            name: Sticker set name
        """
        return await self.call(DeleteStickerSet(
            name=name,
        ))

    async def send_rich_message(
        self,
        chat_id: Union[int, str],
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
        """Use this method to send rich messages. If the message contains a block with a media element, then the bot must have the right to send the media to the chat. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendrichmessage
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent. Bot can send rich messages on behalf of a business account only if the corresponding user can send rich messages.
            chat_id: Unique identifier for the target chat or username of the target bot, supergroup or channel in the format @username
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
        return await self.call(SendRichMessage(
            business_connection_id=business_connection_id,
            chat_id=chat_id,
            message_thread_id=message_thread_id,
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
        ))

    async def send_rich_message_draft(
        self,
        chat_id: int,
        draft_id: int,
        rich_message: InputRichMessage,
        *,
        message_thread_id: Optional[int] = None,
        can_stop: Optional[bool] = None,
        keep_on_stop: Optional[bool] = None,
    ) -> bool:
        """Use this method to stream a partial rich message to a user while the message is being generated. Note that the streamed draft is ephemeral and acts as a temporary 30-second preview - once the output is finalized, you must call sendRichMessage with the complete message to persist it in the user's chat. Returns True on success.
        
        https://core.telegram.org/bots/api#sendrichmessagedraft
        
        Args:
            chat_id: Unique identifier for the target private chat
            message_thread_id: Unique identifier for the target message thread
            draft_id: Unique identifier of the message draft; must be non-zero. Changes to drafts with the same identifier are animated. Otherwise, the draft is replaced without animation.
            rich_message: The partial message to be streamed. Direct upload of new files and explicit upload of files by a URL isn't supported.
            can_stop: Pass True to show the user a button to stop further drafts. The bot will receive an Update "stopped_message_generation" if the user presses the button.
            keep_on_stop: Pass True to keep the draft in the chat when the button is pressed. The draft will still disappear after a short time or if the bot sends a message. To fully preserve the partial draft, the bot should send it as a new message.
        """
        return await self.call(SendRichMessageDraft(
            chat_id=chat_id,
            message_thread_id=message_thread_id,
            draft_id=draft_id,
            rich_message=rich_message,
            can_stop=can_stop,
            keep_on_stop=keep_on_stop,
        ))

    async def answer_inline_query(
        self,
        inline_query_id: str,
        results: List[InlineQueryResult],
        *,
        cache_time: Optional[int] = None,
        is_personal: Optional[bool] = None,
        next_offset: Optional[str] = None,
        button: Optional[InlineQueryResultsButton] = None,
    ) -> bool:
        """Use this method to send answers to an inline query. On success, True is returned.
        
        No more than 50 results per query are allowed.
        
        https://core.telegram.org/bots/api#answerinlinequery
        
        Args:
            inline_query_id: Unique identifier for the answered query
            results: A JSON-serialized Array of results for the inline query
            cache_time: The maximum amount of time in seconds that the result of the inline query may be cached on the server. Defaults to 300.
            is_personal: Pass True if results may be cached on the server side only for the user that sent the query. By default, results may be returned to any user who sends the same query.
            next_offset: Pass the offset that a client should send in the next query with the same text to receive more results. Pass an empty string if there are no more results or if you don't support pagination. Offset length can't exceed 64 bytes.
            button: A JSON-serialized object describing a button to be shown above inline query results
        """
        return await self.call(AnswerInlineQuery(
            inline_query_id=inline_query_id,
            results=results,
            cache_time=cache_time,
            is_personal=is_personal,
            next_offset=next_offset,
            button=button,
        ))

    async def send_invoice(
        self,
        chat_id: Union[int, str],
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
        """Use this method to send invoices. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendinvoice
        
        Args:
            chat_id: Unique identifier for the target chat or username of the target bot, supergroup or channel in the format @username
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
        return await self.call(SendInvoice(
            chat_id=chat_id,
            message_thread_id=message_thread_id,
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
        ))

    async def create_invoice_link(
        self,
        title: str,
        description: str,
        payload: str,
        currency: str,
        prices: List[LabeledPrice],
        *,
        business_connection_id: Optional[str] = None,
        provider_token: Optional[str] = None,
        subscription_period: Optional[int] = None,
        max_tip_amount: Optional[int] = None,
        suggested_tip_amounts: Optional[List[int]] = None,
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
    ) -> str:
        """Use this method to create a link for an invoice. Returns the created invoice link as String on success.
        
        https://core.telegram.org/bots/api#createinvoicelink
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the link will be created. For payments in Telegram Stars only.
            title: Product name, 1-32 characters
            description: Product description, 1-255 characters
            payload: Bot-defined invoice payload, 1-128 bytes. This will not be displayed to the user, use it for your internal processes.
            provider_token: Payment provider token, obtained via @BotFather. Pass an empty string for payments in Telegram Stars.
            currency: Three-letter ISO 4217 currency code, see more on currencies. Pass "XTR" for payments in Telegram Stars.
            prices: Price breakdown, a JSON-serialized list of components (e.g. product price, tax, discount, delivery cost, delivery tax, bonus, etc.). Must contain exactly one item for payments in Telegram Stars.
            subscription_period: The number of seconds the subscription will be active for before the next payment. The currency must be set to "XTR" (Telegram Stars) if the parameter is used. Currently, it must always be 2592000 (30 days) if specified. Any number of subscriptions can be active for a given bot at the same time, including multiple concurrent subscriptions from the same user. Subscription price must no exceed 10000 Telegram Stars.
            max_tip_amount: The maximum accepted amount for tips in the smallest units of the currency (integer, not float/double). For example, for a maximum tip of US$ 1.45 pass max_tip_amount = 145. See the exp parameter in currencies.json, it shows the number of digits past the decimal point for each currency (2 for the majority of currencies). Defaults to 0. Not supported for payments in Telegram Stars.
            suggested_tip_amounts: A JSON-serialized Array of suggested amounts of tips in the smallest units of the currency (integer, not float/double). At most 4 suggested tip amounts can be specified. The suggested tip amounts must be positive, passed in a strictly increased order and must not exceed max_tip_amount.
            provider_data: JSON-serialized data about the invoice, which will be shared with the payment provider. A detailed description of required fields should be provided by the payment provider.
            photo_url: URL of the product photo for the invoice. Can be a photo of the goods or a marketing image for a service.
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
        """
        return await self.call(CreateInvoiceLink(
            business_connection_id=business_connection_id,
            title=title,
            description=description,
            payload=payload,
            provider_token=provider_token,
            currency=currency,
            prices=prices,
            subscription_period=subscription_period,
            max_tip_amount=max_tip_amount,
            suggested_tip_amounts=suggested_tip_amounts,
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
        ))

    async def answer_shipping_query(
        self,
        shipping_query_id: str,
        ok: bool,
        *,
        shipping_options: Optional[List[ShippingOption]] = None,
        error_message: Optional[str] = None,
    ) -> bool:
        """If you sent an invoice requesting a shipping address and the parameter is_flexible was specified, the Bot API will send an Update with a shipping_query field to the bot. Use this method to reply to shipping queries. On success, True is returned.
        
        https://core.telegram.org/bots/api#answershippingquery
        
        Args:
            shipping_query_id: Unique identifier for the query to be answered
            ok: Pass True if delivery to the specified address is possible and False if there are any problems (for example, if delivery to the specified address is not possible)
            shipping_options: Required if ok is True. A JSON-serialized Array of available shipping options.
            error_message: Required if ok is False. Error message in human readable form that explains why it is impossible to complete the order (e.g. "Sorry, delivery to your desired address is unavailable"). Telegram will display this message to the user.
        """
        return await self.call(AnswerShippingQuery(
            shipping_query_id=shipping_query_id,
            ok=ok,
            shipping_options=shipping_options,
            error_message=error_message,
        ))

    async def answer_pre_checkout_query(
        self,
        pre_checkout_query_id: str,
        ok: bool,
        *,
        error_message: Optional[str] = None,
    ) -> bool:
        """Once the user has confirmed their payment and shipping details, the Bot API sends the final confirmation in the form of an Update with the field pre_checkout_query. Use this method to respond to such pre-checkout queries. On success, True is returned. Note: The Bot API must receive an answer within 10 seconds after the pre-checkout query was sent.
        
        https://core.telegram.org/bots/api#answerprecheckoutquery
        
        Args:
            pre_checkout_query_id: Unique identifier for the query to be answered
            ok: Specify True if everything is alright (goods are available, etc.) and the bot is ready to proceed with the order. Use False if there are any problems.
            error_message: Required if ok is False. Error message in human readable form that explains the reason for failure to proceed with the checkout (e.g. "Sorry, somebody just bought the last of our amazing black T-shirts while you were busy filling out your payment details. Please choose a different color or garment!"). Telegram will display this message to the user.
        """
        return await self.call(AnswerPreCheckoutQuery(
            pre_checkout_query_id=pre_checkout_query_id,
            ok=ok,
            error_message=error_message,
        ))

    async def get_my_star_balance(
        self,
    ) -> StarAmount:
        """A method to get the current Telegram Stars balance of the bot. Requires no parameters. On success, returns a StarAmount object.
        
        https://core.telegram.org/bots/api#getmystarbalance
        """
        return await self.call(GetMyStarBalance(
        ))

    async def get_star_transactions(
        self,
        *,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> StarTransactions:
        """Returns the bot's Telegram Star transactions in chronological order. On success, returns a StarTransactions object.
        
        https://core.telegram.org/bots/api#getstartransactions
        
        Args:
            offset: Number of transactions to skip in the response
            limit: The maximum number of transactions to be retrieved. Values between 1-100 are accepted. Defaults to 100.
        """
        return await self.call(GetStarTransactions(
            offset=offset,
            limit=limit,
        ))

    async def refund_star_payment(
        self,
        user_id: int,
        telegram_payment_charge_id: str,
    ) -> bool:
        """Refunds a successful payment in Telegram Stars. Returns True on success.
        
        https://core.telegram.org/bots/api#refundstarpayment
        
        Args:
            user_id: Identifier of the user whose payment will be refunded
            telegram_payment_charge_id: Telegram payment identifier
        """
        return await self.call(RefundStarPayment(
            user_id=user_id,
            telegram_payment_charge_id=telegram_payment_charge_id,
        ))

    async def edit_user_star_subscription(
        self,
        user_id: int,
        telegram_payment_charge_id: str,
        is_canceled: bool,
    ) -> bool:
        """Allows the bot to cancel or re-enable extension of a subscription paid in Telegram Stars. Returns True on success.
        
        https://core.telegram.org/bots/api#edituserstarsubscription
        
        Args:
            user_id: Identifier of the user whose subscription will be edited
            telegram_payment_charge_id: Telegram payment identifier for the subscription
            is_canceled: Pass True to cancel extension of the user subscription; the subscription must be active up to the end of the current subscription period. Pass False to allow the user to re-enable a subscription that was previously canceled by the bot.
        """
        return await self.call(EditUserStarSubscription(
            user_id=user_id,
            telegram_payment_charge_id=telegram_payment_charge_id,
            is_canceled=is_canceled,
        ))

    async def set_passport_data_errors(
        self,
        user_id: int,
        errors: List[PassportElementError],
    ) -> bool:
        """Informs a user that some of the Telegram Passport elements they provided contains errors. The user will not be able to re-submit their Passport to you until the errors are fixed (the contents of the field for which you returned the error must change). Returns True on success.
        
        Use this if the data submitted by the user doesn't satisfy the standards your service requires for any reason. For example, if a birthday date seems invalid, a submitted document is blurry, a scan shows evidence of tampering, etc. Supply some details in the error message to make sure the user knows how to correct the issues.
        
        https://core.telegram.org/bots/api#setpassportdataerrors
        
        Args:
            user_id: User identifier
            errors: A JSON-serialized Array describing the errors
        """
        return await self.call(SetPassportDataErrors(
            user_id=user_id,
            errors=errors,
        ))

    async def send_game(
        self,
        chat_id: Union[int, str],
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
        """Use this method to send a game. On success, the sent Message is returned.
        
        https://core.telegram.org/bots/api#sendgame
        
        Args:
            business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
            chat_id: Unique identifier for the target chat or username of the target bot in the format @username. Games can't be sent to channel direct messages chats and channel chats.
            message_thread_id: Unique identifier for the target message thread (topic) of a forum; for forum supergroups and private chats of bots with forum topic mode enabled only
            game_short_name: Short name of the game, serves as the unique identifier for the game. Set up your games via @BotFather.
            disable_notification: Sends the message silently. Users will receive a notification with no sound.
            protect_content: Protects the contents of the sent message from forwarding and saving
            allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance.
            message_effect_id: Unique identifier of the message effect to be added to the message; for private chats only
            reply_parameters: Description of the message to reply to
            reply_markup: A JSON-serialized object for an inline keyboard. If empty, one 'Play game_title' button will be shown. If not empty, the first button must launch the game.
        """
        return await self.call(SendGame(
            business_connection_id=business_connection_id,
            chat_id=chat_id,
            message_thread_id=message_thread_id,
            game_short_name=game_short_name,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        ))

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
        """Use this method to set the score of the specified user in a game message. On success, if the message is not an inline message, the Message is returned, otherwise True is returned. Returns an error, if the new score is not greater than the user's current score in the chat and force is False.
        
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
        return await self.call(SetGameScore(
            user_id=user_id,
            score=score,
            force=force,
            disable_edit_message=disable_edit_message,
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
        ))

    async def get_game_high_scores(
        self,
        user_id: int,
        *,
        chat_id: Optional[int] = None,
        message_id: Optional[int] = None,
        inline_message_id: Optional[str] = None,
    ) -> List[GameHighScore]:
        """Use this method to get data for high score tables. Will return the score of the specified user and several of their neighbors in a game. Returns an Array of GameHighScore objects.
        
        https://core.telegram.org/bots/api#getgamehighscores
        
        Args:
            user_id: Target user id
            chat_id: Required if inline_message_id is not specified. Unique identifier for the target chat.
            message_id: Required if inline_message_id is not specified. Identifier of the sent message.
            inline_message_id: Required if chat_id and message_id are not specified. Identifier of the inline message.
        """
        return await self.call(GetGameHighScores(
            user_id=user_id,
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
        ))
