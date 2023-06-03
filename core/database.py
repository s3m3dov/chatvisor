from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from config import settings

engine = create_engine(settings.db.uri, echo=True)
session = scoped_session(sessionmaker(bind=engine))
