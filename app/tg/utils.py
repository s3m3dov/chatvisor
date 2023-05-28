from typing import Any, Dict

from langchain.chat_models import ChatOpenAI
from sqlalchemy.sql import insert, select

from app.ai.chatbot import ChatBot
from core.database import engine
from core.entities.enums import SystemUser, Platform
from core.entities.models import PromptMessage, UserChannel, User, OutputMessage

log = print


def ask_chat_openai(llm: ChatOpenAI, question: str) -> str:
    bot = ChatBot(llm=llm)
    response = bot.predict(
        input=question,
        history=None,
    )
    return response


def save_prompt_n_output_to_db(
    platform_user_id: int, prompt: str, output: str, system_sender: SystemUser
) -> None:
    with engine.connect() as conn:
        statement = (
            select(User.id, UserChannel.id)
            .select_from(UserChannel)
            .join(User, onclause=User.id == UserChannel.user_id)
            .where(UserChannel.platform_user_id == platform_user_id)
        )
        result = conn.execute(statement)
        existing_user = result.first()
        sender_id = existing_user[0]
        channel_id = existing_user[1]
        log(f"existing_user: {existing_user}")

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
        log(f"PromptMessage created: {result}")
        prompt_id = result.first()[0]

        statement_3 = insert(OutputMessage).values(
            text=output,
            prompt_id=prompt_id,
            sender_id=system_sender,
        )
        result = conn.execute(statement_3)
        log(f"OutputMessage created: {result}")
        conn.commit()


def get_or_create_user_new(
    platform_user_id: int,
    first_name: str,
    last_name: str,
    data: Dict[str, Any],
) -> Dict[str, Any]:
    user_channel = (
        UserChannel.with_joined(UserChannel.user)
        .where(platform_user_id == platform_user_id)
        .first()
    )
    log(f"user_channel: {user_channel}")

    if not user_channel:
        user = User.create(
            first_name=first_name,
            last_name=last_name,
        )
        log(f"user created: {user}")
        UserChannel.create(
            platform=Platform.TELEGRAM,
            platform_user_id=platform_user_id,
            user_id=user.id,
            data=data,
        )
        is_created = True
        full_name = f"{first_name} {last_name}"
    else:
        is_created = False
        full_name = " ".join(filter(None, [user_channel.user.first_name, user_channel.user.last_name]))

    return {
        "is_created": is_created,
        "full_name": full_name,
    }


def get_or_create_user(
    platform_user_id: int,
    first_name: str,
    last_name: str,
    data: Dict[str, Any],
) -> Dict[str, Any]:
    with engine.connect() as conn:
        statement = (
            select(User.id, User.first_name, User.last_name)
            .select_from(UserChannel)
            .join(User, onclause=User.id == UserChannel.user_id)
            .where(UserChannel.platform_user_id == platform_user_id)
        )
        result = conn.execute(statement)
        existing_user = result.first()

        if not existing_user:
            statement_2 = (
                insert(User)
                .values(
                    first_name=first_name,
                    last_name=last_name,
                )
                .returning(User.id)
            )
            result = conn.execute(statement_2)
            user_id = result.first()[0]
            statement_3 = insert(UserChannel).values(
                platform=Platform.TELEGRAM,
                platform_user_id=platform_user_id,
                user_id=user_id,
                data=data,
            )
            result = conn.execute(statement_3)
            log(f"User created: {result}")
            conn.commit()
            is_created = True
            full_name = f"{first_name} {last_name}"
        else:
            log(f"User exists: {existing_user}")
            is_created = False
            full_name = " ".join(filter(None, existing_user[1:]))

        return {
            "is_created": is_created,
            "full_name": full_name,
        }
