from pydantic import BaseModel


class MessageAutoDeleteTimerChanged(BaseModel):
    message_auto_delete_time: int