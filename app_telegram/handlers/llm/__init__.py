from telegram import Update
from telegram.ext import ContextTypes

from core.config import settings
from .base import base_openai_command, base_openai_ask

__all__ = ["ask_default", "ask_gpt3_5_turbo", "ask_gpt4"]


async def ask_default(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    await base_openai_ask(update, llm_config=settings.gpt3_5_turbo, text=text)


async def ask_gpt3_5_turbo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await base_openai_command(update, context, llm_config=settings.gpt3_5_turbo)


async def ask_gpt4(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await base_openai_command(update, context, llm_config=settings.gpt4)
