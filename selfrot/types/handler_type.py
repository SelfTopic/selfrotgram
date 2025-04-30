from enum import Enum

class HandlerType(Enum):

    message = "message"
    callback_query = "callback_query"
    inline_query = "inline_query"
    base = "base"
