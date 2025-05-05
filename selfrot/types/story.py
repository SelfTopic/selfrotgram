from pydantic import BaseModel


class Story(BaseModel):
    chat: Chat
    id: int