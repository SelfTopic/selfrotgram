from typing import Union, Self
from .paid_media_video import PaidMediaVideo
from .paid_media_photo import PaidMediaPhoto
from .paid_media_preview import PaidMediaPreview

PaidMedia = Union[PaidMediaPreview, PaidMediaPhoto, PaidMediaVideo]