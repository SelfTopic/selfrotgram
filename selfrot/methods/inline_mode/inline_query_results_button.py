from typing import Optional
from pydantic import BaseModel
from ..types import WebAppInfo

class InlineQueryResultsButton(BaseModel):
    text: str
    web_app: Optional[WebAppInfo] = None
    start_parameter: Optional[str] = None