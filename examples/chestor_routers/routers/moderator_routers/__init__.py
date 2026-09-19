"""chestor_bot: src/bot/routers/moderator_routers/__init__.py (ModeratorRouter)"""

from selfrot import BaseRouter

from ...middlewares import ModeratorMiddleware


class ModeratorRouter(BaseRouter):
    middlewares = (ModeratorMiddleware,)
    auto_connect = (
        ".set_rules_router",
        ".set_goodbye_router",
        ".set_welcome_router",
    )


router = ModeratorRouter
