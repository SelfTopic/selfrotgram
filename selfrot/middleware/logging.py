import logging 
import time
from typing import Any
from .base import BaseMiddleware
from ..context import TContext

logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseMiddleware[TContext]):

    after_time: float

    async def pre_handle(self):
        
        self.after_time = time.time()
        return True
    
    async def post_handle(self) -> Any:
        
        ms = int(time.time() - self.after_time)

        logger.info(f"New update on bot id={self.ctx.bot.id} on {ms} ms")
