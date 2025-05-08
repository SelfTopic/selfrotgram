from typing import Union, Self
from pydantic import BaseModel
from .story_area_type import StoryAreaType
from .story_area_position import StoryAreaPosition

class StoryArea(BaseModel):
    position: Union[StoryAreaPosition]
    type: Union[StoryAreaType]