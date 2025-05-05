from pydantic import BaseModel
from .web_app_info import WebAppInfo

class MenuButtonWebApp(BaseModel):
    type: str
    text: str
    web_app: WebAppInfo