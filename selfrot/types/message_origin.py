from typing import Union
from .message_origin_user import MessageOriginUser
from .message_origin_hidden_user import MessageOriginHiddenUser
from .message_origin_chat import MessageOriginChat
from .message_origin_channel import MessageOriginChannel

MessageOrigin = Union[
	MessageOriginUser,
	MessageOriginHiddenUser,
	MessageOriginChat,
	MessageOriginChannel
]