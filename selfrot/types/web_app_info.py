from pydantic import BaseModel

class WebAppInfo(BaseModel):
    url: str