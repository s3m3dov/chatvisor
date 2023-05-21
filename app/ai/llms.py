from langchain.chat_models import ChatOpenAI

from app.core.config import settings

gpt4 = ChatOpenAI(
    model_name="gpt-4",
    max_tokens=settings.max_tokens["gpt-4"],
    temperature=settings.temperature["gpt-4"],
)
gpt3_5_turbo = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    max_tokens=settings.max_tokens["gpt-3.5-turbo"],
    temperature=settings.temperature["gpt-3.5-turbo"],
)
