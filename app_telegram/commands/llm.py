from telegram import Update
from telegram.ext import ContextTypes

from config import settings
from core.ai.main import ChatBotOpenAI
from core.user.main import get_or_create_user_channel
from core.user.plan import PlanLogic
from entities.enums import Platform
from entities.schemas import TelegramUser


async def ask_gpt3_5_turbo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text(
            "You need to ask a question in the format `/gpt3_5_turbo <question>`"
        )
        return

    await update.message.reply_text("Thinking..., this might take a while")
    _user = update.effective_user.to_dict()
    _chat = update.effective_chat.to_dict()
    tg_user = TelegramUser(
        **_user, optional_data={"chat": _chat, "language_code": _user["language_code"]}
    )

    is_created, user_channel = get_or_create_user_channel(platform=Platform.TELEGRAM, data=tg_user)
    plan_logic = PlanLogic(user_id=user_channel.user_id, channel_id=user_channel.id)
    if plan_logic.is_plan_limit_reached():
        await update.message.reply_text(
            "You have reached your plan limit. Please upgrade to premium plan to continue using this feature."
        )
        return

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

    await update.message.reply_text("Thinking..., this might take a while")
    _user = update.effective_user.to_dict()
    _chat = update.effective_chat.to_dict()
    tg_user = TelegramUser(
        **_user, optional_data={"chat": _chat, "language_code": _user["language_code"]}
    )

    is_created, user_channel = get_or_create_user_channel(platform=Platform.TELEGRAM, data=tg_user)
    plan_logic = PlanLogic(user_id=user_channel.user_id, channel_id=user_channel.id)
    if plan_logic.is_plan_limit_reached():
        await update.message.reply_text(
            "You have reached your plan limit. Please upgrade to premium plan to continue using this feature."
        )
        return

    gpt4 = ChatBotOpenAI(user_channel=user_channel, llm_config=settings.gpt4)
    response = await gpt4.ask(question=" ".join(context.args))
    await update.message.reply_text(response)
