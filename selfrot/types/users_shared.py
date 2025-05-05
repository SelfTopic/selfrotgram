from typing import List
from pydantic import BaseModel
from .shared_user import SharedUser

class UsersShared(BaseModel):
    request_id: int
    users: List[SharedUser]