from pydantic import BaseModel


class BotDescription(BaseModel):
    description: str