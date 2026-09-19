"""chestor_bot: src/bot/routers/ghoul_routers/duel/__init__.py (DuelRouter)"""

from selfrot import BaseRouter


class DuelRouter(BaseRouter):
    auto_connect = (
        ".invite_router",
        ".duel_process_router",
    )


router = DuelRouter
