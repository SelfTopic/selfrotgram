from pydantic import BaseModel


class BackgroundTypeChatTheme(BaseModel):
    type: str
    theme_name: str