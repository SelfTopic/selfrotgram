from pydantic import BaseModel
from .message import Message 
from typing import Optional
from .callback import CallbackQuery 

class Update(BaseModel):

    callback: Optional[CallbackQuery] = None 
    message: Optional[Message] = None
    update_id: int 
    edited_message: Optional[Message] = None 
    channel_post: Optional[Message] = None 
    edited_channel_post: Optional[Message] = None
    # business_connection
    business_message: Optional[Message] = None 
    edited_business_message: Optional[Message] = None
    # deleted_business_messages
    # message_reaction
    # message_reaction_count
    # chosen_inline_result
    # inline_query
    # callback_query
    # shipping_query
    # pre_checkout_query
    # purchased_paid_media
    # poll 
    # poll_answer
    # my_chat_member
    # chat_member
    # chat_join_request
    # chat_boost 
    # removed_chat_boost