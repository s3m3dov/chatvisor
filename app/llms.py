from langchain.chat_models import ChatOpenAI

from .config import max_tokens, temperature

gpt4 = ChatOpenAI(
    model_name="gpt-4",
    max_tokens=max_tokens["gpt-4"],
    temperature=temperature["gpt-4"],
)
gpt3_5_turbo = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    max_tokens=max_tokens["gpt-3.5-turbo"],
    temperature=temperature["gpt-3.5-turbo"],
)
