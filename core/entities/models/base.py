from sqlalchemy.orm import DeclarativeBase
from sqlalchemy_mixins import AllFeaturesMixin
from sqlalchemy_mixins.timestamp import TimestampsMixin

from core.database import session


class Base(DeclarativeBase):
    __abstract__ = True


class BaseModel(Base, AllFeaturesMixin):
    __abstract__ = True
    pass


BaseModel.set_session(session)
