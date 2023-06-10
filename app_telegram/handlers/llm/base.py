from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

from core.config.submodels.main import LLMConfig
from core.logging import logger
from entities.enums import Platform
from entities.schemas import TelegramUser
from utils.ai.main import ChatBotOpenAI
from utils.user.checkout import CheckoutSessionCRUD
from utils.user.main import get_or_create_user_channel
from utils.user.plan import PlanLogic

__all__ = ["base_openai_ask", "base_openai_command"]


async def base_openai_ask(update: Update, llm_config: LLMConfig, text: str) -> None:
    await update.message.reply_text("Thinking..., this might take a while")
    _user = update.effective_user.to_dict()
    _chat = update.effective_chat.to_dict()
    tg_user = TelegramUser(
        **_user, optional_data={"chat": _chat, "language_code": _user["language_code"]}
    )

    is_created, user_channel = get_or_create_user_channel(
        platform=Platform.TELEGRAM, data=tg_user
    )

    plan_logic = PlanLogic(user_id=user_channel.user_id, channel_id=user_channel.id)
    if plan_logic.is_plan_limit_reached():
        is_subscribed, session = CheckoutSessionCRUD.create_checkout_session(
            user_channel.user
        )
        if is_subscribed:
            await update.message.reply_text("You have reached your plan limit. Try again later.")
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

    openai_llm = ChatBotOpenAI(user_channel=user_channel, llm_config=llm_config)
    response = await openai_llm.ask(question=text)
    await update.message.reply_text(response)


async def base_openai_command(
        update: Update, context: ContextTypes.DEFAULT_TYPE, llm_config: LLMConfig
) -> None:
    logger.debug(update.message.text)
    if not context.args:
        await update.message.reply_text(
            "You haven't entered a prompt. " "E.g., `/[command] <question>`"
        )
        return
    text = " ".join(context.args)
    await base_openai_ask(update, llm_config=llm_config, text=text)
