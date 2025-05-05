from pydantic import BaseModel


class StoryAreaTypeUniqueGift(BaseModel):
    type: str
    name: str