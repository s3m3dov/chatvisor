from langchain import LLMChain
from langchain.base_language import BaseLanguageModel
from langchain.prompts.prompt import PromptTemplate

from app.ai.constants import TEMPLATE


class ChatBot:
    """
    This is a chatbot that uses the OpenAI API
    to generate responses to prompts.
    """

    def __init__(self, llm: BaseLanguageModel) -> None:
        # self.embeddings = OpenAIEmbeddings()
        self.engine = LLMChain(
            llm=llm,
            prompt=PromptTemplate(
                input_variables=["history", "input"],
                template=TEMPLATE,
            ),
            verbose=True,
        )

    def predict(self, *args, **kwargs) -> str:
        return self.engine.predict(*args, **kwargs)
