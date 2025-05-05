from pydantic import BaseModel
from .video import Video

class PaidMediaVideo(BaseModel):
    type: str
    video: Video