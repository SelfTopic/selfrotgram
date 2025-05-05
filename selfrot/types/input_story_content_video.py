from typing import Optional
from pydantic import BaseModel


class InputStoryContentVideo(BaseModel):
    type: str
    video: str
    duration: Optional[float] = None
    cover_frame_timestamp: Optional[float] = None
    is_animation: Optional[bool] = None