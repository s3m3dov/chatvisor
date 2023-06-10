from langchain.chat_models import ChatOpenAI

from core.config import settings
from core.config.submodels.main import LLMConfig
from core.logging import logger
from entities.models import UserChannel, PromptMessage, OutputMessage
from .base import BaseAgent

__all__ = ["ChatBotOpenAI"]


class ChatBotOpenAI:
    """
    This is a chatbot that uses the OpenAI API
    to generate responses to prompts.
    """

    def __init__(self, user_channel: UserChannel, llm_config: LLMConfig):
        self.llm_config = llm_config
        self.bot = BaseAgent(llm=self.init_llm())
        self.user_channel = user_channel

    def init_llm(self) -> ChatOpenAI:
        llm = ChatOpenAI(
            openai_api_key=settings.openapi_key,
            model_name=self.llm_config.name.value,
            max_tokens=self.llm_config.max_tokens,
            temperature=self.llm_config.temperature,
        )
        return llm

    async def ask(self, question: str) -> str:
        response, prompt_tokens, completion_tokens, cost = self.bot.predict(
            input=question,
            history=None,
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
        )
        logger.info(f"PromptMessage created: {prompt_message}")
        return prompt_message

    @staticmethod
    async def save_output(output: str, prompt_message: PromptMessage) -> None:
        OutputMessage.create(
            text=output,
            prompt_id=prompt_message.id,
        )
        logger.info(f"PromptMessage created: {prompt_message}")
