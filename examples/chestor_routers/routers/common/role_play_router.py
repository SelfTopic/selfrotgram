"""chestor_bot: src/bot/routers/common/role_play_router.py"""

from selfrot import BaseRouter

from ...middlewares import RpCommandsMiddleware


class RolePlayRouter(BaseRouter):
    middlewares = (RpCommandsMiddleware,)


router = RolePlayRouter
