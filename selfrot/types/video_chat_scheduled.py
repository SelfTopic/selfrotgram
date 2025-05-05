from pydantic import BaseModel


class VideoChatScheduled(BaseModel):
    start_date: int