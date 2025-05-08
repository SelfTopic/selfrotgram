from pydantic import BaseModel

class BotName(BaseModel):
    name: str