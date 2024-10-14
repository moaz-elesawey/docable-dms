import uuid

from sqlalchemy import PrimaryKeyConstraint
from sqlmodel import Field, SQLModel


class Responsibility(SQLModel, table=True):
    __tablename__ = "responsibilities"

    group_id: uuid.UUID = Field(foreign_key="groups.group_id", nullable=False)

    document_id: uuid.UUID = Field(foreign_key="documents.document_id", nullable=False)

    __table_args__ = (PrimaryKeyConstraint("group_id", "document_id"),)
