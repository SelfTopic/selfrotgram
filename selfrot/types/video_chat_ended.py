from pydantic import BaseModel

class VideoChatEnded(BaseModel):
    duration: int