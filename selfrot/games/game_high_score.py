from pydantic import BaseModel
from ..types.user import User


class GameHighScore(BaseModel):
	position: int
	user: User
	score: int