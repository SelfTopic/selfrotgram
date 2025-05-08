from typing import Union, Self
from .owned_gift_regular import OwnedGiftRegular
from .owned_gift_unique import OwnedGiftUnique

OwnedGift = Union[OwnedGiftRegular, OwnedGiftUnique]