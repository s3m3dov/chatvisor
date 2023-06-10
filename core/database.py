from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from core.config import settings
from core.logging import logger

__all__ = ["session"]


def create_session() -> scoped_session:
    try:
        engine = create_engine(
            settings.db.uri,
            echo=True,
            pool_pre_ping=True,
            pool_size=20,
            pool_timeout=10,
            connect_args={"connect_timeout": 5},
        )
        _session = scoped_session(sessionmaker(bind=engine))
        return _session
    except Exception as exc_msg:
        logger.exception(exc_msg)


session = create_session()
