from langchain.chat_models import ChatOpenAI

from entities.config_schemas.main import LLMConfig
from entities.models import UserChannel, PromptMessage, OutputMessage
from .base import BaseAgent

log = print

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
            model_name=self.llm_config.name.value,
            max_tokens=self.llm_config.max_tokens,
            temperature=self.llm_config.temperature,
        )
        return llm

    async def ask(self, question: str) -> str:
        response, prompt_tokens, completion_tokens = self.bot.predict(
            input=question,
            history=None,
        )
        prompt_message = await self.save_prompt(
            prompt=question,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
        )
        await self.save_output(output=response, prompt_message=prompt_message)

        return response

    async def save_prompt(
        self, prompt: str, prompt_tokens: int, completion_tokens: int
    ) -> PromptMessage:
        prompt_message = PromptMessage.create(
            text=prompt,
            sender_id=self.user_channel.user_id,
            channel_id=self.user_channel.id,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
        )
        log(f"PromptMessage created: {prompt_message}")
        return prompt_message

    async def save_output(self, output: str, prompt_message: PromptMessage) -> None:
        OutputMessage.create(
            text=output,
            prompt_id=prompt_message.id,
            sender_id=self.llm_config.name,
        )
        log(f"PromptMessage created: {prompt_message}")
