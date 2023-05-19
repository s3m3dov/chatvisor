from dotenv import dotenv_values
from telegram.ext import ApplicationBuilder, Application

from app.commands import command_handlers, command_info

config = dotenv_values(".env")


async def post_init(application: Application) -> None:
    bot = application.bot
    await bot.set_my_commands(commands=command_info)


if __name__ == "__main__":
    app = (
        ApplicationBuilder()
        .token(config["TELEGRAM_BOT_TOKEN"])
        .post_init(post_init)
        .build()
    )
    app.add_handlers(command_handlers)
    app.run_polling()
