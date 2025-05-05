from typing import List, Optional
from pydantic import BaseModel
from .poll_option import PollOption
from .message_entity import MessageEntity

class Poll(BaseModel):
    id: str
    question: str
    question_entities: Optional[List[MessageEntity]] = None
    options: List[PollOption]
    total_voter_count: int
    is_closed: bool
    is_anonymous: bool
    type: str
    allows_multiple_answers: bool
    correct_option_id: Optional[int] = None
    explanation: Optional[str] = None
    explanation_entities: Optional[List[MessageEntity]] = None
    open_period: Optional[int] = None
    close_date: Optional[int] = None