from sqlalchemy.orm import selectinload
from telegram import Bot

from core.config import settings
from core.database import session_scope
from core.logging import logger
from entities.enums import Platform
from entities.models import User, UserChannel

bot = Bot(token=settings.telegram.bot_token)


async def send_telegram_message(customer_id: str, message: str):
    with session_scope() as session:
        user_channel = (
            session.query(UserChannel)
            .join(User)
            .filter(
                User.customer_id == customer_id,
                UserChannel.platform == Platform.TELEGRAM,
            )
            .options(selectinload(UserChannel.user))
            .first()
        )

        if not user_channel:
            logger.error(f"User channel not found: {customer_id}")
            return

        await bot.send_message(
            chat_id=user_channel.platform_user_id,
            text=message,
        )
