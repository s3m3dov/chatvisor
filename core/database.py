from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from config import settings

engine = create_engine(settings.database_url, echo=True)
session = scoped_session(sessionmaker(bind=engine))
