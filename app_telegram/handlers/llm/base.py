from telegram import Update
from telegram.ext import ContextTypes

from core.config.submodels.main import LLMConfig
from utils.ai.main import ChatBotOpenAI
from utils.telegram import get_or_create_user_tg_channel, is_plan_limit_reached

__all__ = ["base_openai_ask", "base_openai_command"]


async def base_openai_ask(update: Update, llm_config: LLMConfig, text: str) -> None:
    is_created, user_channel = get_or_create_user_tg_channel(update)
    await is_plan_limit_reached(update, user_channel)

    await update.message.reply_text("Thinking...")
    openai_llm = ChatBotOpenAI(user_channel=user_channel, llm_config=llm_config)
    response = await openai_llm.ask(question=text)
    await update.message.reply_text(response)


async def base_openai_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE, llm_config: LLMConfig
) -> None:
    if not context.args:
        await update.message.reply_text(
            "You haven't entered a prompt. " "E.g., `/[command] <question>`"
        )
        return
    text = " ".join(context.args)
    await base_openai_ask(update, llm_config=llm_config, text=text)
