import openai
from telegram import Update
from telegram.ext import ContextTypes
from core.logging import logger
from core.config import settings

__all__ = ["ask_dalle"]


# from utils.telegram import get_or_create_user_tg_channel


async def ask_dalle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text(
            "You haven't entered a prompt. " "E.g., `/[command] <question>`"
        )
        return

    text = " ".join(context.args)
    logger.debug(f"ask_dalle: {text}")
    # is_created, user_channel = get_or_create_user_tg_channel(update)
    response = openai.Image.create(
        prompt=text,
        api_key=settings.openapi_key,
        n=1,
        size="1024x1024"
    )
    logger.debug(f"ask_dalle: {response}")
    image_url = response['data'][0]['url']
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=image_url,
        caption=text,
    )
