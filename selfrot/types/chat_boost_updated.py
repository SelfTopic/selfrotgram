from pydantic import BaseModel
from .chat_boost import ChatBoost

class ChatBoostUpdated(BaseModel):
    chat: Chat
    boost: ChatBoost