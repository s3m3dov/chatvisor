from sqlmodel import create_engine

from app.core.config import settings
from .models import (
    Message,
    User,
    UserChannel,
)

engine = create_engine(settings.database_url, echo=True)