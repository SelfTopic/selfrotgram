from pydantic import BaseModel
from ..types import User


class GameHighScore(BaseModel):
	position: int
	user: User
	score: int