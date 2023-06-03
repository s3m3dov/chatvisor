from langchain.chat_models import ChatOpenAI

from core.ai.chatbot import ChatBot

log = print


def ask_chat_openai(llm: ChatOpenAI, question: str) -> str:
    bot = ChatBot(llm=llm)
    response = bot.predict(
        input=question,
        history=None,
    )
    return response
