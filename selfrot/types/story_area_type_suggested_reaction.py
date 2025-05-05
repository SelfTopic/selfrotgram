from typing import Optional
from pydantic import BaseModel
from .reaction_type import ReactionType

class StoryAreaTypeSuggestedReaction(BaseModel):
    type: str
    reaction_type: ReactionType
    is_dark: Optional[bool] = None
    is_flipped: Optional[bool] = None