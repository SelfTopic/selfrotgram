from pydantic import BaseModel

class ReactionTypeCustomEmoji(BaseModel):
    type: str
    custom_emoji_id: str