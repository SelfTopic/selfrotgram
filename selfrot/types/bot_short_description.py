from pydantic import BaseModel


class BotShortDescription(BaseModel):
    short_description: str