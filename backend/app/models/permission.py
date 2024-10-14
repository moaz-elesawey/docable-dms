import uuid

from sqlmodel import Field, SQLModel


class PermissionBase(SQLModel):
    name: str = Field(max_length=255, nullable=False, unique=True, index=True)
    codename: str = Field(max_length=255, nullable=False, unique=True, index=True)
    flag: int = Field(nullable=False, unique=True, index=True)
    description: str = Field(max_length=255, nullable=False, default="N/A")


class PermissionCreate(PermissionBase):
    description: str | None = Field(max_length=255, default="N/A")


class PermissionUpdate(PermissionBase):
    name: str | None = Field(max_length=255, unique=True, index=True)
    codename: str | None = Field(max_length=255, unique=True, index=True)
    flag: int | None = Field(unique=True, index=True)
    description: str | None = Field(max_length=255, default="N/A")


class Permission(PermissionBase, table=True):
    __tablename__ = "permissions"

    permission_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


class PermissionPublic(PermissionBase):
    permission_id: uuid.UUID


class PermissionListPublic(SQLModel):
    data: list[PermissionPublic]
    count: int
