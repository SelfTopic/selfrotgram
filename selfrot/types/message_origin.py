from typing import Union, Self
from .message_origin_user import MessageOriginUser
from .message_origin_channel import MessageOriginChannel
from .message_origin_chat import MessageOriginChat
from .message_origin_hidden_user import MessageOriginHiddenUser

MessageOrigin = Union[MessageOriginUser, MessageOriginHiddenUser, MessageOriginChat, MessageOriginChannel]