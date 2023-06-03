from sqlalchemy.orm import DeclarativeBase
from sqlalchemy_mixins.activerecord import ActiveRecordMixin
from sqlalchemy_mixins.repr import ReprMixin
from sqlalchemy_mixins.serialize import SerializeMixin
from sqlalchemy_mixins.smartquery import SmartQueryMixin

from core.database import session


class Base(DeclarativeBase):
    __abstract__ = True


class BaseModel(Base, ActiveRecordMixin, SmartQueryMixin, ReprMixin, SerializeMixin):
    __abstract__ = True
    pass


BaseModel.set_session(session)
