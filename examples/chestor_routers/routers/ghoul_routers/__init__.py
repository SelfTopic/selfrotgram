"""chestor_bot: src/bot/routers/ghoul_routers/__init__.py (GhoulRouter)"""

from selfrot import BaseRouter

from ...middlewares import GhoulMiddleware


class GhoulRouter(BaseRouter):
    middlewares = (GhoulMiddleware,)
    auto_connect = (
        ".upgrade_kagune",
        ".snap",
        ".tops",
        ".coffee",
        ".quiz",
        ".upgrade_stat",
        ".passive_status",
        ".eat_human",
        ".mob_fight",
        ".duel",
        ".combat_power",
    )


router = GhoulRouter
