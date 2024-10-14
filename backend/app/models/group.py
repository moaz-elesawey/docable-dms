import uuid

from sqlmodel import Field, SQLModel


class GroupBase(SQLModel):
    name: str = Field(max_length=255, nullable=False, unique=True, index=True)
    abbreviation: str = Field(max_length=255, nullable=False, unique=True, index=True)


class GroupCreate(GroupBase):
    pass


class GroupUpdate(GroupBase):
    name: str | None = Field(default=None, max_length=255)
    abbreviation: str | None = Field(default=None, max_length=255)


class Group(GroupBase, table=True):
    __tablename__ = "groups"

    group_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


class GroupPublic(GroupBase):
    group_id: uuid.UUID


class GroupListPublic(SQLModel):
    data: list[GroupPublic]
    count: int
