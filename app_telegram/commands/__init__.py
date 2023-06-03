from telegram import BotCommand
from telegram.ext import CommandHandler

from .llm import (
    ask_gpt3_5_turbo,
    ask_gpt4,
)
from .main import (
    start,
    echo,
    subscribe,
)

command_handlers = [
    CommandHandler("start", start),
    CommandHandler("subscribe", subscribe),
    CommandHandler("gpt3_5_turbo", ask_gpt3_5_turbo),
    CommandHandler("gpt4", ask_gpt4),
    CommandHandler("echo", echo),
]
command_info = [
    BotCommand("start", "Start the bot"),
    BotCommand("subscribe", "Subscribe to the premium plan"),
    BotCommand("gpt3_5_turbo", "Ask GPT-3.5 Turbo a question"),
    BotCommand("gpt4", "Ask GPT-4 a question"),
    BotCommand("echo", "Echo the message"),
]
