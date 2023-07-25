import openai
import pendulum
from telegram import Update
from telegram.ext import ContextTypes

from core.config import settings

__all__ = ["ask_dalle"]

from entities.models import PromptMessage, OutputMessage

from utils.telegram import get_or_create_user_tg_channel, is_plan_limit_reached


async def ask_dalle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text(
            "You haven't entered a prompt. " "E.g., `/[command] <question>`"
        )
        return

    text = " ".join(context.args)
    is_created, user_channel = get_or_create_user_tg_channel(update)

    is_limit_reached = await is_plan_limit_reached(update, user_channel)

    if not is_limit_reached:
        await update.message.reply_text("Generating...")

        dalle_conf = settings.dalle
        prompt_message = PromptMessage.create(
            text=text,
            sender_id=user_channel.user_id,
            receiver_id=dalle_conf.name,
            channel_id=user_channel.id,
            prompt_tokens=0,
            completion_tokens=0,
            cost=dalle_conf.price,
            created_at=pendulum.now("UTC").int_timestamp,
        )
        response = openai.Image.create(
            prompt=text,
            api_key=settings.openapi_key,
            n=1,
            size=settings.dalle.resolution
        )
        image_url = response['data'][0]['url']
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=image_url,
            caption=text,
        )
        OutputMessage.create(
            text=image_url,
            prompt_id=prompt_message.id,
            created_at=pendulum.now("UTC").int_timestamp,
        )
