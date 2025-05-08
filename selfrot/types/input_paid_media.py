from typing import Union, Self
from .input_paid_media_video import InputPaidMediaVideo
from .input_paid_media_photo import InputPaidMediaPhoto

InputPaidMedia = Union[InputPaidMediaPhoto, InputPaidMediaVideo]