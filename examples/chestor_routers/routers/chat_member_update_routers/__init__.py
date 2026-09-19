"""chestor_bot: src/bot/routers/chat_member_update_routers/__init__.py (UpdateChatMemberRouter)"""

from selfrot import BaseRouter


class UpdateChatMemberRouter(BaseRouter):
    auto_connect = (
        ".left_chat_member",
        ".new_chat_member",
    )


router = UpdateChatMemberRouter
