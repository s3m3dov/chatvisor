from typing import Tuple

from langchain import ConversationChain
from langchain.base_language import BaseLanguageModel
from langchain.callbacks import get_openai_callback
from langchain.memory import ConversationSummaryBufferMemory
from langchain.prompts import PromptTemplate

from core.logging import logger
from utils.ai.constants import TEMPLATE


class BaseChatAgent:
    """
    This is a chatbot that uses the OpenAI API
    to generate responses to prompts.
    """

    def __init__(self, llm: BaseLanguageModel) -> None:
        # self.embeddings = OpenAIEmbeddings()
        self.engine = ConversationChain(
            llm=llm,
            prompt=PromptTemplate(
                input_variables=["history", "input"],
                template=TEMPLATE,
            ),
            memory=ConversationSummaryBufferMemory(llm=llm, max_token_limit=650),
            verbose=True,
        )

    def predict(self, *args, **kwargs) -> Tuple[str, int, int, float]:
        with get_openai_callback() as cb:
            result = self.engine.predict(*args, **kwargs)
            prompt_tokens = cb.prompt_tokens
            completion_tokens = cb.completion_tokens
            total_cost = round(cb.total_cost, 4)
            logger.info(
                f"Total Tokens: {cb.total_tokens}\n"
                f"Prompt Tokens: {prompt_tokens}\n"
                f"Completion Tokens: {completion_tokens}\n"
                f"Total Cost (USD): ${cb.total_cost}\n"
            )

        return result, prompt_tokens, completion_tokens, total_cost
