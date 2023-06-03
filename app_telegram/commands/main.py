from telegram import Update
from telegram.constants import ChatType
from telegram.ext import ContextTypes

from config import settings
from core.crud.user import (
    get_or_create_user,
    get_user_channel, get_customer, create_checkout_session,
)
from entities.schemas import TelegramUser, TelegramChat


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = (
        " ".join(context.args) if context.args else "You didn't say anything!"
    )
    await update.message.reply_text(message)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    tg_user = TelegramUser(**update.effective_user.to_dict())
    tg_chat = TelegramChat(**update.effective_chat.to_dict())

    platform_user_id = tg_user.id

    if tg_chat.type != ChatType.PRIVATE.value:
        await update.message.reply_text(
            "It's only possible to use this bot in private chats."
        )
        return

    result = get_or_create_user(
        platform_user_id=platform_user_id,
        first_name=tg_user.first_name,
        last_name=tg_user.last_name,
        data={"chat": tg_chat.dict()},
    )
    if result["is_created"]:
        await update.message.reply_text(f"Welcome, {result['full_name']}!")
    else:
        await update.message.reply_text(
            f"Welcome back, {result['full_name']}!"
        )


async def subscribe(
        update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    user_channel = get_user_channel(platform_user_id=update.effective_user.id)
    customer = get_customer(user_id=user_channel.user_id)
    session = create_checkout_session(customer_id=customer.id)
    await update.message.reply_text(
        f"You can subscribe here: {session.url}"
    )
