from telegram.ext import ApplicationBuilder, Application

from core.config import settings
from core.logging import logger
from .handlers import (
    command_handlers,
    command_info,
    error_handler,
    message_handler,
)


async def post_init(application: Application) -> None:
    bot = application.bot
    await bot.set_my_commands(commands=command_info)


def start_bot() -> None:
    logger.critical("Starting bot...")
    app = (
        ApplicationBuilder()
        .token(settings.telegram.bot_token)
        .post_init(post_init)
        .build()
    )
    app.add_handlers(command_handlers)
    app.add_handler(message_handler)
    app.add_error_handler(error_handler)
    logger.critical("Bot started!")
    app.run_polling()
