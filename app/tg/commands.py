from telegram import Update
from telegram.constants import ChatType
from telegram.ext import ContextTypes

from app.ai.llms import gpt3_5_turbo, gpt4
from app.db.enums import SystemUser
from app.db.schemas import TelegramUser, TelegramChat
from app.tg.utils import ask_chat_openai, save_prompt_n_output_to_db, get_or_create_user


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
        await update.message.reply_text(f"Welcome back, {result['full_name']}!")


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"Hello {update.effective_user.first_name}")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = " ".join(context.args) if context.args else "You didn't say anything!"
    await update.message.reply_text(message)


async def ask_gpt3_5_turbo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text(
            "You need to ask a question in the format `/gpt3_5_turbo <question>`"
        )
        return

    platform_user_id = update.effective_user.id
    await update.message.reply_text("Thinking..., this might take a while")
    question = " ".join(context.args)
    response = ask_chat_openai(llm=gpt3_5_turbo, question=question)
    await update.message.reply_text(response)
    save_prompt_n_output_to_db(
        platform_user_id=platform_user_id,
        prompt=question,
        output=response,
        system_sender=SystemUser.GPT_3_5_TURBO,
    )


async def ask_gpt4(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text(
            "You need to ask a question in the format `/gpt4 <question>`"
        )
        return

    platform_user_id = update.effective_user.id
    await update.message.reply_text("Thinking..., this might take a while")
    question = " ".join(context.args)
    response = ask_chat_openai(llm=gpt4, question=question)
    await update.message.reply_text(response)
    save_prompt_n_output_to_db(
        platform_user_id=platform_user_id,
        prompt=question,
        output=response,
        system_sender=SystemUser.GPT_4,
    )


async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    pass
