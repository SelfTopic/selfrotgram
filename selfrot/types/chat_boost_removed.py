from pydantic import BaseModel
from .chat import Chat
from .chat_boost_source import ChatBoostSource

class ChatBoostRemoved(BaseModel):
    chat: Chat
    boost_id: str
    remove_date: int
    source: ChatBoostSource