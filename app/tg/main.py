from telegram.ext import ApplicationBuilder, Application

from core.config import settings
from app.tg import command_handlers, command_info

log = print


async def post_init(application: Application) -> None:
    bot = application.bot
    await bot.set_my_commands(commands=command_info)


def start_bot() -> None:
    log("Starting bot...")
    app = (
        ApplicationBuilder()
        .token(settings.telegram_bot_token)
        .post_init(post_init)
        .build()
    )
    app.add_handlers(command_handlers)
    log("Bot started!")
    app.run_polling()
