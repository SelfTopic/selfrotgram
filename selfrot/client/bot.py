from ..methods import TelegramAPIMethod, SendMessage, GetUpdates
from .session import AsyncSession
from typing import Optional
import asyncio 

class Bot:

    session: AsyncSession
    token: str
    
    def __init__(
        self, 
        token: Optional[str] = None
    ):
        self.token = token 
        self.session = AsyncSession()

    async def get_updates(self) -> None:
        method = GetUpdates(token=self.token)

        await self._make_request(method=method)

    async def send_message(self, text: str, chat_id: int) -> None:
        method = SendMessage(
            text=text,
            chat_id=chat_id    
        )

        await self._make_request(method=method)

    async def _make_request(self, method: type[TelegramAPIMethod]):
        return await self.session(method=method, token=self.token)

if __name__ == '__main__':
    bot = Bot("8105695330:AAFz3vOdQQXnnL5y2uXIMWuoM8h-JXekOaM")

    async def main():
        await bot.send_message("Hello", 7970396690)

    asyncio.run(main())