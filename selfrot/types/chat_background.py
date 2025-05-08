from pydantic import BaseModel
from .background_type import BackgroundType

class ChatBackground(BaseModel):
    type: BackgroundType