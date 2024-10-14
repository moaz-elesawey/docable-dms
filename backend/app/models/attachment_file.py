import uuid

from sqlmodel import Field, SQLModel


class AttachmentFile(SQLModel, table=True):
    __tablename__ = "attachment_files"

    attachment_file_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    document_id: uuid.UUID = Field(foreign_key="documents.document_id", nullable=True)

    revision_id: uuid.UUID = Field(foreign_key="revisions.revision_id", nullable=True)

    attachment_id: uuid.UUID = Field(
        foreign_key="attachments.attachment_id", nullable=True
    )
