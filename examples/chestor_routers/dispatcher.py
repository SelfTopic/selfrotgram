from selfrot import BaseContext, BaseDispatcher, Bot
from selfrot.middleware import LoggingMiddleware

from .middlewares import BanMiddleware, DatabaseMiddleware, SyncEntitiesMiddleware


class AppDispatcher(BaseDispatcher[BaseContext]):
    bot = Bot
    context = BaseContext

    # Порядок как в chestor_bot/__main__.py: первый — самый внешний.
    middlewares = (
        LoggingMiddleware,
        DatabaseMiddleware,
        SyncEntitiesMiddleware,
        BanMiddleware,
    )

    # Порядок как в chestor_bot/routers/routes.py (include_routers).
    auto_connect = (
        ".routers.common.start_router",
        ".routers.common.bot_router",
        ".routers.common.error_router",
        ".routers.ghoul_routers",
        ".routers.common.check_balance",
        ".routers.common.help_router",
        ".routers.common.profile_router",
        ".routers.common.race_profile_router",
        ".routers.moderator_routers",
        ".routers.common.check_rules_router",
        ".routers.chat_member_update_routers",
        ".routers.creator_routers",
        ".routers.common.tops",
        ".routers.common.role_play_router",
        ".routers.common.wordle_router",
        ".routers.common.anime_router",
        ".routers.common.transfer_router",
        ".routers.common.dep_router",
        ".routers.common.fun_router",
    )
