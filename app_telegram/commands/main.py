from telegram import Update
from telegram.constants import ChatType
from telegram.ext import ContextTypes

from config import settings
from core.user.checkout import CheckoutSessionCRUD
from core.user.main import (
    get_or_create_user,
    get_user_channel,
)
from entities.enums import Platform
from entities.schemas import TelegramUser


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = " ".join(context.args) if context.args else "You didn't say anything!"
    await update.message.reply_text(message)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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

    is_created, user = get_or_create_user(platform=Platform.TELEGRAM, data=tg_user)
    if is_created:
        await update.message.reply_text(f"Welcome, {user.full_name}!")
    else:
        await update.message.reply_text(f"Welcome back, {user.full_name}!")


async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_channel = get_user_channel(platform_user_id=update.effective_user.id)
    is_subscribed, session = CheckoutSessionCRUD.create_checkout_session(
        user_channel.user
    )

    if is_subscribed:
        await update.message.reply_text("You are already subscribed, enjoy!")
    else:
        await update.message.reply_text(f"You can subscribe here: {session.url}")


async def manage_subscription(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    user_channel = get_user_channel(platform_user_id=update.effective_user.id)
    is_subscribed, session = CheckoutSessionCRUD.create_checkout_session(
        user_channel.user
    )

    if is_subscribed:
        await update.message.reply_text(
            f"Manage your subscription here: {settings.dashboard_url}"
        )
    else:
        await update.message.reply_text(
            f"You are not subscribed yet, please subscribe here: {session.url}"
        )
