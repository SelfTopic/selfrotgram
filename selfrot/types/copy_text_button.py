from pydantic import BaseModel


class CopyTextButton(BaseModel):
    text: str