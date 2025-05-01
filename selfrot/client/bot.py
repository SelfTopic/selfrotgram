from ..methods import TelegramAPIMethod, SendMessage, GetUpdates
from .session import AsyncSession
from ..config import ConfigAPI
from typing import Optional 
from ..types import Update 


class Bot:

    session: AsyncSession
    token: str
    
    def __init__(
        self, 
        token: Optional[str] = None,
    ):
        
        self.token = token if token else "Unauthorized"
        self.session = AsyncSession()
        self.cfg = ConfigAPI()
        self.id: int = 0

        if self.token == "Unauthorized":

            token = self.cfg.get_token()
            if not token:
                raise Exception("Fill bot token in configure file")
            
            self.token = token

        self.id = int(self.token.split(":")[0])

    async def get_updates(self, offset: int = 0):
        method = GetUpdates(
            offset=offset
        )

        response = await self._get_request(method=method)

        updates = [Update(**u) for u in response.get("result", [])]
        return updates

    async def send_message(self, text: str, chat_id: int):
        method = SendMessage(
            text=text,
            chat_id=chat_id    
        )

        response = await self._make_request(method=method)
        return response

    async def _make_request(self, method: TelegramAPIMethod):
        return await self.session(method=method, token=self.token)
    
    async def _get_request(self, method: TelegramAPIMethod):
        return await self.session.get(method=method, token=self.token)

    
  