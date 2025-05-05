from typing import Any, Dict, Tuple

class TelegramAPIMethod:
    __api_method__: str 
    data: dict[str, Any]

    def __init__(self, *args: Tuple[Any], **kwargs: Dict[str, Any]):
        attributes = self.__annotations__.keys()

        for i, arg in enumerate(args):
            setattr(self, list(attributes)[i], arg)

        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def data(self) -> Dict[str, Any]:
        data = {}
        for attr_name in self.__annotations__:
            if attr_name != "__api_method__":
                data[attr_name] = getattr(self, attr_name)
        return data