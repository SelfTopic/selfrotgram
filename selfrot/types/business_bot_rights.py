from typing import Optional
from pydantic import BaseModel


class BusinessBotRights(BaseModel):
    can_reply: Optional[bool] = None
    can_read_messages: Optional[bool] = None
    can_delete_sent_messages: Optional[bool] = None
    can_delete_all_messages: Optional[bool] = None
    can_edit_name: Optional[bool] = None
    can_edit_bio: Optional[bool] = None
    can_edit_profile_photo: Optional[bool] = None
    can_edit_username: Optional[bool] = None
    can_change_gift_settings: Optional[bool] = None
    can_view_gifts_and_stars: Optional[bool] = None
    can_convert_gifts_to_stars: Optional[bool] = None
    can_transfer_and_upgrade_gifts: Optional[bool] = None
    can_transfer_stars: Optional[bool] = None
    can_manage_stories: Optional[bool] = None