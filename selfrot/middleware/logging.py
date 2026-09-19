import logging
import time
from typing import Any

from ..context import TContext
from .base import BaseMiddleware

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseMiddleware[TContext]):
    """Время обработки апдейта (вместе со всеми мидлварями внутри) и его исход."""

    started: float

    async def pre_handle(self) -> bool:
        self.started = time.monotonic()
        return True

    async def post_handle(self, exc: BaseException | None = None) -> Any:
        ms = int((time.monotonic() - self.started) * 1000)
        user = self.ctx.user
        who = f"user id={user.id}" if user is not None else "no user"

        if exc is not None:
            logger.info(f"Update from {who} failed after {ms} ms: {exc!r}")
        else:
            logger.info(f"Update from {who} handled in {ms} ms")
