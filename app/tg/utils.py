from langchain.chat_models import ChatOpenAI
from sqlalchemy.sql import insert, select

from app.ai.chatbot import ChatBot
from app.db import engine
from app.db.enums import SystemUser
from app.db.models import PromptMessage, UserChannel, User, OutputMessage


def ask_chat_openai(llm: ChatOpenAI, question: str) -> str:
    bot = ChatBot(llm=llm)
    response = bot.predict(
        input=question,
        history=None,
    )
    return response


def save_prompt_n_output_to_db(platform_chat_id: int, prompt: str, output: str, system_sender: SystemUser) -> None:
    with engine.connect() as conn:
        statement = (
            select(User.id, UserChannel.id)
            .select_from(UserChannel)
            .join(User, onclause=User.id == UserChannel.user_id)
            .where(UserChannel.platform_chat_id == platform_chat_id)
        )
        result = conn.execute(statement)
        existing_user = result.first()
        sender_id = existing_user[0]
        channel_id = existing_user[1]
        print(existing_user, "existing_user")

        statement_2 = (
            insert(PromptMessage)
            .values(
                text=prompt,
                sender_id=sender_id,
                channel_id=channel_id,

            )
            .returning(
                PromptMessage.id,
            )
        )
        result = conn.execute(statement_2)
        print(result)
        prompt_id = result.first()[0]

        statement_3 = (
            insert(OutputMessage)
            .values(
                text=output,
                prompt_id=prompt_id,
                sender_id=system_sender,
            )
        )
        result = conn.execute(statement_3)
        print(result)
        conn.commit()
