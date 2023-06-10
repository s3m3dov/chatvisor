from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.constants import ChatType
from telegram.ext import ContextTypes

from core.config import settings
from core.logging import logger
from entities.enums import Platform
from entities.schemas import TelegramUser
from utils.user.checkout import CheckoutSessionCRUD
from utils.user.main import get_or_create_user_channel


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.debug(f"Started app: {update.effective_user.username}")

    if update.effective_chat.type != ChatType.PRIVATE.value:
        await update.message.reply_text(
            "It's only possible to use this bot in private chats."
        )
        return

    _user = update.effective_user.to_dict()
    _chat = update.effective_chat.to_dict()
    tg_user = TelegramUser(
        **_user, optional_data={"chat": _chat, "language_code": _user["language_code"]}
    )

    is_created, user_channel = get_or_create_user_channel(
        platform=Platform.TELEGRAM, data=tg_user
    )
    user = user_channel.user
    if is_created:
        await update.message.reply_text(f"Welcome, {user.full_name}!")
    else:
        await update.message.reply_text(f"Welcome back, {user.full_name}!")


async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    _user = update.effective_user.to_dict()
    _chat = update.effective_chat.to_dict()
    tg_user = TelegramUser(
        **_user, optional_data={"chat": _chat, "language_code": _user["language_code"]}
    )

    is_created, user_channel = get_or_create_user_channel(
        platform=Platform.TELEGRAM, data=tg_user
    )
    is_subscribed, session = CheckoutSessionCRUD.create_checkout_session(
        user_channel.user
    )

    if is_subscribed:
        await update.message.reply_text("You are already subscribed, enjoy!")
    else:
        await update.message.reply_text(
            "You are not subscribed yet, please subscribe here",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Subscribe",
                            url=session.url,
                        )
                    ]
                ]
            ),
        )


async def manage_subscription(
        update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    _user = update.effective_user.to_dict()
    _chat = update.effective_chat.to_dict()
    tg_user = TelegramUser(
        **_user, optional_data={"chat": _chat, "language_code": _user["language_code"]}
    )

    is_created, user_channel = get_or_create_user_channel(
        platform=Platform.TELEGRAM, data=tg_user
    )
    is_subscribed, session = CheckoutSessionCRUD.create_checkout_session(
        user_channel.user
    )

    if is_subscribed:
        await update.message.reply_text(
            "Manage your subscription here",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Subscription Dashboard",
                            url=settings.stripe.dashboard_url,
                        )
                    ]
                ]
            ),
        )
    else:
        await update.message.reply_text(
            "You are not subscribed yet, please subscribe here",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Subscribe",
                            url=session.url,
                        )
                    ]
                ]
            ),
        )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = " ".join(context.args) if context.args else "You didn't say anything!"
    await update.message.reply_text(message)
