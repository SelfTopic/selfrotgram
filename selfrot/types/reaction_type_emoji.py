from pydantic import BaseModel


class ReactionTypeEmoji(BaseModel):
    type: str
    emoji: str