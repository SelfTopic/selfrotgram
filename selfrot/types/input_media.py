from typing import Union, Self
from .input_media_document import InputMediaDocument
from .input_media_photo import InputMediaPhoto
from .input_media_animation import InputMediaAnimation
from .input_media_video import InputMediaVideo
from .input_media_audio import InputMediaAudio

InputMedia = Union[InputMediaAnimation, InputMediaDocument, InputMediaAudio, InputMediaPhoto, InputMediaVideo]