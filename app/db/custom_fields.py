import uuid as uuid_lib

from sqlmodel import Field

IntPrimaryKey = Field(
    default=None,
    primary_key=True,
    index=True,
    allow_mutation=False,
    nullable=False,
)

UUIDPrimaryKey = Field(
    default=None,
    default_factory=uuid_lib.uuid4,
    primary_key=True,
    index=True,
    allow_mutation=False,
    nullable=False,
)
