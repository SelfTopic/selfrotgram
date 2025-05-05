from pydantic import BaseModel
from .user import User

class ProximityAlertTriggered(BaseModel):
    traveler: User
    watcher: User
    distance: int