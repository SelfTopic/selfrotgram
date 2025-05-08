from typing import Union
from .inaccessible_message import InaccessibleMessage
from .message import Message

MaybeInaccessibleMessage = Union[Message, InaccessibleMessage]