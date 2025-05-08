from typing import Union, Self
from .input_story_content_video import InputStoryContentVideo
from .input_story_content_photo import InputStoryContentPhoto

InputStoryContent = Union[InputStoryContentPhoto, InputStoryContentVideo]