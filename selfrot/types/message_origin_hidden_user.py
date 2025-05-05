from pydantic import BaseModel


class MessageOriginHiddenUser(BaseModel):
    type: str
    date: int
    sender_user_name: str