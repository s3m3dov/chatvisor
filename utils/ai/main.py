from datetime import datetime
from typing import List

from langchain.schema import BaseMessage, HumanMessage, AIMessage

from core.config import settings
from core.config.submodels.main import LLMConfig
from core.database import session_scope
from core.logging import logger
from entities.enums import SystemUser
from entities.models import UserChannel, PromptMessage, OutputMessage
from .base import BaseChatAgent

__all__ = ["ChatBotOpenAI"]


class ChatBotOpenAI:
    """
    This is a chatbot that uses the OpenAI API
    to generate responses to prompts.
    """

    def __init__(self, user_channel: UserChannel, llm_config: LLMConfig):
        self.user_channel = user_channel
        self.llm_config = llm_config
        self.bot = BaseChatAgent(
            llm_config=llm_config,
            messages=self.get_chat_history(),
        )

    async def ask(self, question: str) -> str:
        response, prompt_tokens, completion_tokens, cost = self.bot.predict(
            input=question
        )
        prompt_message = await self.save_prompt(
            prompt=question,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            cost=cost,
        )
        await self.save_output(output=response, prompt_message=prompt_message)

        return response

    async def save_prompt(
            self, prompt: str, prompt_tokens: int, completion_tokens: int, cost: float
    ) -> PromptMessage:
        prompt_message = PromptMessage.create(
            text=prompt,
            sender_id=self.user_channel.user_id,
            receiver_id=self.llm_config.name,
            channel_id=self.user_channel.id,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            cost=cost,
            created_at=datetime.utcnow().timestamp(),
        )
        logger.info(f"PromptMessage created: {prompt_message}")
        return prompt_message

    @staticmethod
    async def save_output(output: str, prompt_message: PromptMessage) -> None:
        OutputMessage.create(
            text=output,
            prompt_id=prompt_message.id,
            created_at=datetime.utcnow().timestamp(),
        )

    def get_chat_history(self) -> List[BaseMessage]:
        _messages = self._get_messages_from_db()
        messages = []
        for _msg in _messages[::-1]:
            messages.append(HumanMessage(content=_msg[0]))
            messages.append(AIMessage(content=_msg[1]))
        return messages

    def _get_messages_from_db(self) -> str:
        with session_scope() as session:
            messages = (
                session.query(PromptMessage.text, OutputMessage.text)
                .join(OutputMessage, PromptMessage.id == OutputMessage.prompt_id)
                .filter(
                    PromptMessage.receiver_id.in_(SystemUser.get_llms()),
                    PromptMessage.sender_id == self.user_channel.user_id,
                )
                .order_by(PromptMessage.created_at.desc(), PromptMessage.id.desc())
                .limit(settings.limit)
            )
            return messages
