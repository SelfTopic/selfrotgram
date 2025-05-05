from typing import Union
from .input_paid_media_photo import InputPaidMediaPhoto
from .input_paid_media_video import InputPaidMediaVideo

InputPaidMedia = Union[
	InputPaidMediaPhoto,
	InputPaidMediaVideo
]