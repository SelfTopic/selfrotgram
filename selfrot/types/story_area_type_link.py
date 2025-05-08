from pydantic import BaseModel

class StoryAreaTypeLink(BaseModel):
    type: str
    url: str