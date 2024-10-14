import uuid

from sqlmodel import Field, SQLModel


class Attachment(SQLModel, table=True):
    __tablename__ = "attachments"

    attachment_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    document_id: uuid.UUID = Field(foreign_key="documents.document_id", nullable=True)

    revision_id: uuid.UUID = Field(foreign_key="revisions.revision_id", nullable=True)

    draft_attachment_id: uuid.UUID = Field(
        foreign_key="draft_attachments.draft_attachment_id", nullable=True
    )
