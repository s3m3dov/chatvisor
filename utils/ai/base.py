from typing import Tuple, List, Optional

from langchain import ConversationChain
from langchain.base_language import BaseLanguageModel
from langchain.callbacks import get_openai_callback
from langchain.chat_models import ChatOpenAI
from langchain.memory import (
    ConversationSummaryBufferMemory,
    ChatMessageHistory, ConversationBufferWindowMemory,
)
from langchain.memory.chat_memory import BaseChatMemory
from langchain.prompts import PromptTemplate
from langchain.schema import BaseMessage

from core.config import settings
from core.config.submodels.main import LLMConfig
from core.logging import logger
from utils.ai.constants import TEMPLATE


class BaseChatAgent:
    """
    This is a chatbot that uses the OpenAI API
    to generate responses to prompts.
    """

    def __init__(
        self, llm_config: LLMConfig, messages: Optional[List[BaseMessage]]
    ) -> None:
        self.llm_config = llm_config
        self.llm = self._init_llm(llm_config)
        self.memory = self._init_memory(messages)
        self.engine = self._init_chain()

    @staticmethod
    def _init_llm(llm_config: LLMConfig) -> BaseLanguageModel:
        llm = ChatOpenAI(
            openai_api_key=settings.openapi_key,
            model_name=llm_config.name.value,
            max_tokens=llm_config.max_tokens,
            temperature=llm_config.temperature,
        )
        return llm

    def _init_memory(
        self, messages: Optional[List[BaseMessage]]
    ) -> Optional[BaseChatMemory]:
        if not messages:
            return None
        logger.debug("Messages: %s", messages)
        memory = ConversationBufferWindowMemory(
            chat_memory=ChatMessageHistory(messages=messages),
            k=self.llm_config.buffer_size,
        )
        return memory

    def _init_chain(self) -> ConversationChain:
        chain = ConversationChain(
            llm=self.llm,
            memory=self.memory,
            verbose=True,
            prompt=PromptTemplate(
                input_variables=["history", "input"],
                template=TEMPLATE,
            ),
        )
        return chain

    def predict(self, *args, **kwargs) -> Tuple[str, int, int, float]:
        with get_openai_callback() as cb:
            result = self.engine.predict(*args, **kwargs)
            prompt_tokens = cb.prompt_tokens
            completion_tokens = cb.completion_tokens
            total_cost = round(cb.total_cost, 4)
            logger.info(
                "Total Tokens: %d\n"
                "Prompt Tokens: %d\n"
                "Completion Tokens: %d\n"
                "Total Cost (USD): $%.4f\n",
                cb.total_tokens,
                prompt_tokens,
                completion_tokens,
                cb.total_cost,
            )

        return result, prompt_tokens, completion_tokens, total_cost
