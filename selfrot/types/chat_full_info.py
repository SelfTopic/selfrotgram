from typing import List, Optional
from pydantic import BaseModel
from .chat import Chat
from .birthdate import Birthdate
from .accepted_gift_types import AcceptedGiftTypes
from .chat_location import ChatLocation
from .business_intro import BusinessIntro
from .reaction_type import ReactionType
from .business_location import BusinessLocation
from .chat_photo import ChatPhoto
from .chat_permissions import ChatPermissions
from .message import Message
from .business_opening_hours import BusinessOpeningHours

class ChatFullInfo(BaseModel):
    id: int
    type: str
    title: Optional[str] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_forum: Optional[bool] = None
    accent_color_id: int
    max_reaction_count: int
    photo: Optional[ChatPhoto] = None
    active_usernames: Optional[List[str]] = None
    birthdate: Optional[Birthdate] = None
    business_intro: Optional[BusinessIntro] = None
    business_location: Optional[BusinessLocation] = None
    business_opening_hours: Optional[BusinessOpeningHours] = None
    personal_chat: Optional[Chat] = None
    available_reactions: Optional[List[ReactionType]] = None
    background_custom_emoji_id: Optional[str] = None
    profile_accent_color_id: Optional[int] = None
    profile_background_custom_emoji_id: Optional[str] = None
    emoji_status_custom_emoji_id: Optional[str] = None
    emoji_status_expiration_date: Optional[int] = None
    bio: Optional[str] = None
    has_private_forwards: Optional[bool] = None
    has_restricted_voice_and_video_messages: Optional[bool] = None
    join_to_send_messages: Optional[bool] = None
    join_by_request: Optional[bool] = None
    description: Optional[str] = None
    invite_link: Optional[str] = None
    pinned_message: Optional[Message] = None
    permissions: Optional[ChatPermissions] = None
    accepted_gift_types: AcceptedGiftTypes
    can_send_paid_media: Optional[bool] = None
    slow_mode_delay: Optional[int] = None
    unrestrict_boost_count: Optional[int] = None
    message_auto_delete_time: Optional[int] = None
    has_aggressive_anti_spam_enabled: Optional[bool] = None
    has_hidden_members: Optional[bool] = None
    has_protected_content: Optional[bool] = None
    has_visible_history: Optional[bool] = None
    sticker_set_name: Optional[str] = None
    can_set_sticker_set: Optional[bool] = None
    custom_emoji_sticker_set_name: Optional[str] = None
    linked_chat_id: Optional[int] = None
    location: Optional[ChatLocation] = None