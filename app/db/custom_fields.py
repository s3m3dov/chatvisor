import uuid as uuid_lib

from sqlmodel import Field

IntPrimaryKey = Field(
    default=None,
    primary_key=True,
    index=True,
    nullable=False,
)

UUIDPrimaryKey = Field(
    default_factory=uuid_lib.uuid4,
    primary_key=True,
    index=True,
    nullable=False,
)
