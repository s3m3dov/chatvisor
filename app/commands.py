from telegram import Update, BotCommand
from telegram.ext import ContextTypes, CommandHandler


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(update.message.text)


command_handlers = [
    CommandHandler("hello", hello),
    CommandHandler("echo", echo),
]
command_info = [
    BotCommand("hello", "Say hello to the bot"),
    BotCommand("echo", "Echo the message"),
]
