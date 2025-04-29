from .base import TelegramAPIMethod 


class SendMessage(TelegramAPIMethod):
    __api_method__ = "sendMessage"
    chat_id: int 
    user_id: int

    def __init__(self, text: str, chat_id: int):
        super().__init__()
        self.text = text
        self.chat_id = chat_id
        self.data = {
            "text": text,
            "chat_id": chat_id    
        }
         

    