import asyncio
import logging
import os

from .dispatcher import AppDispatcher


async def main() -> None:
    dp = AppDispatcher(token=os.environ.get("BOT_TOKEN"))
    await dp.setup()
    await dp.polling()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    asyncio.run(main())
