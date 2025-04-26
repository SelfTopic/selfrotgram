import aiohttp 
from ..methods import TelegramAPIMethod
from typing import Optional
from .telegram import TELEGRAM_API
import json

class AsyncSession:
    session: aiohttp.ClientSession
    
    def __init__(
        self, 
        session: Optional[aiohttp.ClientSession] = None,
        *args
    ):
        self.session = session 
        

    async def create_session(self):
        self.session = self.session if self.session else aiohttp.ClientSession()

    async def __call__(self, method: TelegramAPIMethod, token: str, *args, **kwds):
        
        await self.create_session()

        url = TELEGRAM_API.get_url(
            token=token,
            method=method
        )

        
        response = await self.session.post(url=url, data=method.data)
        
        dumps = json.dumps(await response.json(), indent=4)
        print(dumps)

        return response



