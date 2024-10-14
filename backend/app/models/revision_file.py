import uuid

from sqlmodel import Field, SQLModel


class RevisionFile(SQLModel, table=True):
    __tablename__ = "revision_files"

    revision_file_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    document_id: uuid.UUID = Field(foreign_key="documents.document_id", nullable=True)

    revision_id: uuid.UUID = Field(foreign_key="revisions.revision_id", nullable=True)
