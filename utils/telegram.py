from typing import Tuple, Optional

from telegram import Update

from entities.enums import Platform
from entities.models import UserChannel
from entities.schemas import TelegramUser
from utils.user.main import get_or_create_user_channel

__all__ = ["get_or_create_user_tg_channel"]


def get_or_create_user_tg_channel(update: Update) -> Tuple[bool, Optional[UserChannel]]:
    """
    Create or get user channel from telegram update
    Args:
        update (Update): telegram update
    Returns:
        Tuple[bool, Optional[UserChannel]]: is_created, user_channel
    """
    _user = update.effective_user.to_dict()
    _chat = update.effective_chat.to_dict()
    tg_user = TelegramUser(
        **_user, optional_data={"chat": _chat, "language_code": _user["language_code"]}
    )

    is_created, user_channel = get_or_create_user_channel(
        platform=Platform.TELEGRAM, data=tg_user
    )
    return is_created, user_channel
