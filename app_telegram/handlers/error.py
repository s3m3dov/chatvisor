import html
import json
import traceback

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from core.config import settings
from core.logging import logger


async def error_handler(
    update: object, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Log the error and send a telegram message to notify the developer."""
    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__
    )
    tb_string = "".join(tb_list)[-3000:]
    logger.error("Exception while handling an update:", exc_info=tb_string)

    # Build the message with some markup and additional information about what happened.
    # You might need to add some logic to deal with messages longer than the 4096-character limit.
    update_str = (
        update.to_dict() if isinstance(update, Update) else str(update)
    )
    message = (
        f"An exception was raised while handling an update\n"
        f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}"
        "</pre>\n\n"
        f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n"
        f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n"
        f"<pre>{html.escape(tb_string)}</pre>"
    )

    # Finally, send the message
    await context.bot.send_message(
        chat_id=settings.telegram.developer_chat_id,
        text=message,
        parse_mode=ParseMode.HTML,
    )


async def bad_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Raise an error to trigger the error handler."""
    await context.bot.wrong_method_name()  # type: ignore[attr-defined]
