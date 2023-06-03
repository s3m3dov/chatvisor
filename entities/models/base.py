from sqlalchemy.orm import DeclarativeBase
from sqlalchemy_mixins import AllFeaturesMixin

from core.database import session


class Base(DeclarativeBase):
    __abstract__ = True


class BaseModel(Base, AllFeaturesMixin):
    __abstract__ = True
    pass


BaseModel.set_session(session)
