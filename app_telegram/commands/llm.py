from telegram import Update
from telegram.ext import ContextTypes

from core.ai.llms import gpt3_5_turbo, gpt4
from core.ai.main import ask_chat_openai
from core.crud.user import (
    save_prompt_n_output,
)
from entities.enums import SystemUser


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
    save_prompt_n_output(
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
    save_prompt_n_output(
        platform_user_id=platform_user_id,
        prompt=question,
        output=response,
        system_sender=SystemUser.GPT_4,
    )
