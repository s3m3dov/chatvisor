from telegram import Update
from telegram.ext import ContextTypes

from config import settings
from core.ai.main import ChatBotOpenAI
from core.user.main import get_user_channel


async def ask_gpt3_5_turbo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text(
            "You need to ask a question in the format `/gpt3_5_turbo <question>`"
        )
        return

    await update.message.reply_text("Thinking..., this might take a while")

    user_channel = get_user_channel(platform_user_id=update.effective_user.id)
    gpt3_5_turbo = ChatBotOpenAI(
        user_channel=user_channel, llm_config=settings.gpt3_5_turbo
    )
    response = await gpt3_5_turbo.ask(question=" ".join(context.args))
    await update.message.reply_text(response)


async def ask_gpt4(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text(
            "You need to ask a question in the format `/gpt4 <question>`"
        )
        return

    user_channel = get_user_channel(platform_user_id=update.effective_user.id)
    got4 = ChatBotOpenAI(user_channel=user_channel, llm_config=settings.gpt4)
    response = await got4.ask(question=" ".join(context.args))
    await update.message.reply_text(response)
