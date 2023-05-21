from telegram import Update, BotCommand
from telegram.ext import ContextTypes, CommandHandler

from app.ai.chatbot import ChatBot
from app.ai.llms import gpt4, gpt3_5_turbo


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = " ".join(context.args) if context.args else "You didn't say anything!"
    await update.message.reply_text(message)


async def whoami(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    chat = update.effective_chat
    data = {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "language_code": user.language_code,
        "is_bot": user.is_bot,
        "is_premium": user.is_premium,
        "chat_id": chat.id,
        "chat_type": chat.type,
        "chat_title": chat.title,
        "chat_username": chat.username,
    }
    await update.message.reply_text(
        f"""
        User: {user}
        Chat: {chat}
        Data: {data}
        """
    )


async def ask_gpt3_5_turbo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("You need to ask a question in the format `/gpt3_5_turbo <question>`")
        return

    await update.message.reply_text("Thinking...")
    question = " ".join(context.args)
    bot = ChatBot(llm=gpt3_5_turbo)
    response = bot.predict(
        input=question,
        history=None,
    )
    await update.message.reply_text(response)


async def ask_gpt4(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("You need to ask a question in the format `/gpt4 <question>`")
        return

    await update.message.reply_text("Thinking...")
    question = " ".join(context.args)
    bot = ChatBot(llm=gpt4)
    response = bot.predict(
        input=question,
        history=None,
    )
    await update.message.reply_text(response)


command_handlers = [
    CommandHandler("hello", hello),
    CommandHandler("echo", echo),
    CommandHandler("whoami", whoami),
    CommandHandler("gpt3_5_turbo", ask_gpt3_5_turbo),
    CommandHandler("gpt4", ask_gpt4),
]
command_info = [
    BotCommand("hello", "Say hello to the bot"),
    BotCommand("echo", "Echo the message"),
    BotCommand("whoami", "Show details about myself"),
    BotCommand("gpt3_5_turbo", "Ask GPT-3.5 Turbo a question"),
    BotCommand("gpt4", "Ask GPT-4 a question"),
]
