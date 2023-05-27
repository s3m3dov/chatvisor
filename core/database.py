from sqlalchemy import create_engine

from core.config import settings
from core.entities.models import (
    PromptMessage,
    OutputMessage,
    User,
    UserChannel,
)

engine = create_engine(settings.database_url, echo=True)
