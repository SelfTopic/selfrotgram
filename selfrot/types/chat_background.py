from pydantic import BaseModel


class ChatBackground(BaseModel):
    type: BackgroundType