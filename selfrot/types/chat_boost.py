from pydantic import BaseModel
from .chat_boost_source import ChatBoostSource

class ChatBoost(BaseModel):
    boost_id: str
    add_date: int
    expiration_date: int
    source: ChatBoostSource