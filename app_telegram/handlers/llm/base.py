from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

from core.config.submodels.main import LLMConfig
from utils.ai.main import ChatBotOpenAI
from utils.telegram import get_or_create_user_tg_channel
from utils.user.plan import UserPlan

__all__ = ["base_openai_ask", "base_openai_command"]


async def base_openai_ask(update: Update, llm_config: LLMConfig, text: str) -> None:
    is_created, user_channel = get_or_create_user_tg_channel(update)
    user_plan = UserPlan(user_id=user_channel.user_id, channel_id=user_channel.id)

    if user_plan.is_plan_limit_reached():
        is_subscribed, session = user_plan.create_checkout_session(user_channel.user)
        if is_subscribed:
            await update.message.reply_text(
                "You have reached your plan limit. Try again later."
            )
        else:
            await update.message.reply_text(
                "Upgrade to the premium plan if you don't want limits to hold you back!",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="Upgrade Now",
                                url=session.url,
                            )
                        ]
                    ]
                ),
            )
        return

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
