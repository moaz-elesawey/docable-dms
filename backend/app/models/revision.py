import uuid

from sqlmodel import Field, SQLModel


class Revision(SQLModel, table=True):
    __tablename__ = "revisions"

    revision_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    document_id: uuid.UUID = Field(foreign_key="documents.document_id", nullable=True)

    draft_id: uuid.UUID = Field(foreign_key="drafts.draft_id", nullable=True)
