from typing import Optional, List
from pydantic import BaseModel
from ..types import PhotoSize
from ..types import MessageEntity
from ..types import Animation

class Game(BaseModel):
	title: str
	description: str
	photo: List[PhotoSize]
	text: Optional[str] = None
	text_entities: Optional[List[MessageEntity]] = None
	animation: Optional[Animation] = None