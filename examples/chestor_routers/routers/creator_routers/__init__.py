"""chestor_bot: src/bot/routers/creator_routers/__init__.py (CreatorRouter)"""

from selfrot import BaseRouter

from ...middlewares import CreatorMiddleware


class CreatorRouter(BaseRouter):
    middlewares = (CreatorMiddleware,)
    auto_connect = (
        ".media",
        ".ban",
        ".players_lookup",
        ".stats_edits",
        ".reset",
        ".broadcast",
        ".level_up",
        ".kagune_admin",
        ".kill",
        ".cooldown_admin",
    )


router = CreatorRouter
