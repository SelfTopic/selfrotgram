from pydantic import BaseModel


class ReactionCount(BaseModel):
    type: ReactionType
    total_count: int