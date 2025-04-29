from typing import Optional
from dataclasses import dataclass 

@dataclass
class User:
    id: int 
    first_name: str 
    is_bot: bool 
    language_code: str
    last_name: Optional[str] = None 
    username: Optional[str] = None

    @property 
    def full_name(self) -> str:
        return self.first_name + self.last_name if self.last_name else ""

