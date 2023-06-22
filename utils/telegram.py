from typing import Tuple, Optional

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton

from entities.enums import Platform
from entities.models import UserChannel
from entities.schemas import TelegramUser
from utils.user.main import get_or_create_user_channel
from utils.user.plan import UserPlan

__all__ = ["get_or_create_user_tg_channel", "is_plan_limit_reached"]


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


async def is_plan_limit_reached(update: Update, user_channel: UserChannel) -> bool:
    user_plan = UserPlan(user_id=user_channel.user_id, channel_id=user_channel.id)

    if user_plan.is_plan_limit_reached():
        is_subscribed, session = user_plan.create_checkout_session(user_channel.user)
        if is_subscribed:
            await update.message.reply_text(
                "You have reached your plan limit. Try again later."
            )
        else:
            await update.message.reply_text(
                "Upgrade to the premium plan if you don't want limits to hold you back!",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="Upgrade Now",
                                url=session.url,
                            )
                        ]
                    ]
                ),
            )
        return True
    return False
