from pydantic import BaseModel


class ReactionTypePaid(BaseModel):
    type: str