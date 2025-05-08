from pydantic import BaseModel
from .reaction_type import ReactionType

class ReactionCount(BaseModel):
    type: ReactionType
    total_count: int