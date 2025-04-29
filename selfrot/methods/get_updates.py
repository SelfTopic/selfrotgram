from .base import TelegramAPIMethod 



class GetUpdates(TelegramAPIMethod):
    __api_method__ = "getUpdates"
    offset: int

    def __init__(self, offset: int) -> None:
        self.offset = offset 

        self.data = {
            "offset": self.offset
        }