import aiohttp 
from ..methods import TelegramAPIMethod
from typing import Optional
from .telegram import TELEGRAM_API


class AsyncSession:
    session: Optional[aiohttp.ClientSession]
    
    def __init__(
        self, 
        session: Optional[aiohttp.ClientSession] = None,
    ):
        self.session = session if session else None
        
    async def create_session(self):
        self.session = self.session if self.session else aiohttp.ClientSession()

    async def __call__(self, method: TelegramAPIMethod, token: str):

        await self.create_session()
        url = TELEGRAM_API.get_url(
            token=token,
            method=method
        )
        if self.session:
            response = await self.session.post(url=url, data=method.data, ssl=False)

            return await response.json()
        
        raise

    async def get(self, method: TelegramAPIMethod, token: str):

        await self.create_session()
        url = TELEGRAM_API.get_url(
            token=token,
            method=method    
        )

        if self.session:
            response = await self.session.get(url=url, data=method.data, ssl=False)

            return await response.json()
        
        raise

    async def delete(self, method: TelegramAPIMethod, token: str):

        await self.create_session()
        url = TELEGRAM_API.get_url(
            token=token,
            method=method
        )

        if self.session:
            response = await self.session.delete(url=url, ssl=False)

            return response
        
        raise