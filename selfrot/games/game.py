from typing import Optional, List
from pydantic import BaseModel
from ..types.photo_size import PhotoSize
from ..types.message_entity import MessageEntity
from ..types.animation import Animation

class Game(BaseModel):
	title: str
	description: str
	photo: List[PhotoSize]
	text: Optional[str] = None
	text_entities: Optional[List[MessageEntity]] = None
	animation: Optional[Animation] = None