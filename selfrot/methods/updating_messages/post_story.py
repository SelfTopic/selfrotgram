from typing import Union, List, Optional, ClassVar
from ..base import TelegramAPIMethod
from dataclasses import dataclass
from ..types import InputStoryContent
from ..types import MessageEntity
from ..types import [StoryArea

@dataclass
class PostStory(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "postStory"
    business_connection_id: str
    content: Union[InputStoryContent]
    active_period: int
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    areas: Optional[Union[List[StoryArea]]] = None
    post_to_chat_page: Optional[bool] = None
    protect_content: Optional[bool] = None