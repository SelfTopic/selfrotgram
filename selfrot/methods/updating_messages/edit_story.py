from typing import Union, List, Optional, ClassVar
from ..base import TelegramAPIMethod
from dataclasses import dataclass
from ..types import InputStoryContent
from ..types import MessageEntity
from ..types import [StoryArea

@dataclass
class EditStory(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "editStory"
    business_connection_id: str
    story_id: int
    content: Union[InputStoryContent]
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    areas: Optional[Union[List[StoryArea]]] = None