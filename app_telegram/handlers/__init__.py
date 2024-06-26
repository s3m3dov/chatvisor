from telegram import BotCommand
from telegram.ext import CommandHandler, filters, MessageHandler

from .error import error_handler
from .general import start, echo, subscribe, manage_subscription
from .llm import ask_gpt3_5_turbo, ask_gpt4, ask_default
from .llm.base import base_openai_ask
from .image import ask_dalle

__all__ = ["error_handler", "message_handler", "command_handlers", "command_info"]

command_handlers = [
    CommandHandler("start", start),
    CommandHandler("subscribe", subscribe),
    CommandHandler("gpt3_5_turbo", ask_gpt3_5_turbo),
    CommandHandler("gpt4", ask_gpt4),
    CommandHandler("dalle", ask_dalle),
    CommandHandler("echo", echo),
    CommandHandler("manage_subscription", manage_subscription),
]
command_info = [
    BotCommand("start", "Start the bot"),
    BotCommand("subscribe", "Subscribe to the premium plan"),
    BotCommand("gpt3_5_turbo", "Ask GPT-3.5 Turbo a question"),
    BotCommand("gpt4", "Ask GPT-4 a question"),
    BotCommand("dalle", "Generate image from text via DALL-E"),
    BotCommand("echo", "Echo the message"),
    BotCommand("manage_subscription", "Manage your subscription"),
]
message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, ask_default)
