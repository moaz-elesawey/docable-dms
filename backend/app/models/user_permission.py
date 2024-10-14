import uuid

from sqlalchemy import PrimaryKeyConstraint
from sqlmodel import Field, SQLModel


class UserPermission(SQLModel, table=True):
    __tablename__ = "user_permissions"

    user_id: uuid.UUID = Field(foreign_key="users.user_id", nullable=False)

    permission_id: uuid.UUID = Field(
        foreign_key="permissions.permission_id", nullable=False
    )

    __table_args__ = (PrimaryKeyConstraint("user_id", "permission_id"),)
