from pydantic import BaseModel


class MessageId(BaseModel):
    message_id: int