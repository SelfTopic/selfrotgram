from pydantic import BaseModel


class InaccessibleMessage(BaseModel):
    chat: Chat
    message_id: int
    date: int