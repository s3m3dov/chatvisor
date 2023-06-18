from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings
from core.logging import logger

__all__ = ["engine", "session_scope"]

engine = create_engine(
    settings.db_url,
    echo=True,
    pool_pre_ping=True,
    pool_size=20,
    connect_args={"connect_timeout": 10},
)


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations"""

    _session_maker = sessionmaker(bind=engine)
    _session = _session_maker()

    try:
        yield _session
        _session.commit()
    except Exception as exc_msg:
        logger.exception(exc_msg)
        _session.rollback()
        raise
    finally:
        _session.close()
