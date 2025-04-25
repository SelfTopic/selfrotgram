from ..methods import TelegramAPIMethod, SendMessage, GetUpdates
from .session import AsyncSession

class Bot:

    session: AsyncSession
    token: str
    
    def __init__(self):
        pass

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
        await self.session(method=method)

