from pydantic import BaseModel


class WebAppData(BaseModel):
    data: str
    button_text: str