import uuid

from sqlmodel import Field, SQLModel


class Audit(SQLModel, table=True):
    __tablename__ = "audits"

    audit_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    user_id: uuid.UUID = Field(foreign_key="users.user_id", nullable=True)
