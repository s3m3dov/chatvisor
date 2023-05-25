from telegram import BotCommand
from telegram.ext import CommandHandler

from app.tg.commands import (
    start,
    hello,
    echo,
    ask_gpt3_5_turbo,
    ask_gpt4,

)

command_handlers = [
    CommandHandler("start", start),
    CommandHandler("hello", hello),
    CommandHandler("echo", echo),
    CommandHandler("gpt3_5_turbo", ask_gpt3_5_turbo),
    CommandHandler("gpt4", ask_gpt4),
]
command_info = [
    BotCommand("start", "Start the bot"),
    BotCommand("hello", "Say hello to the bot"),
    BotCommand("echo", "Echo the message"),
    BotCommand("gpt3_5_turbo", "Ask GPT-3.5 Turbo a question"),
    BotCommand("gpt4", "Ask GPT-4 a question"),
]
