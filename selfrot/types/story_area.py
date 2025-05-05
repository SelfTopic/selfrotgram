from typing import Union
from pydantic import BaseModel
from .story_area_type import StoryAreaType

class StoryArea(BaseModel):
    position: Union[StoryAreaPosition]
    type: Union[StoryAreaType]