import uuid

from sqlalchemy import PrimaryKeyConstraint
from sqlmodel import Field, SQLModel


class GroupPermission(SQLModel, table=True):
    __tablename__ = "group_permissions"

    group_id: uuid.UUID = Field(foreign_key="groups.group_id", nullable=False)

    permission_id: uuid.UUID = Field(
        foreign_key="permissions.permission_id", nullable=False
    )

    __table_args__ = (PrimaryKeyConstraint("group_id", "permission_id"),)
