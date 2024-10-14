import uuid

from sqlmodel import Field, SQLModel


class DraftAttachmentFile(SQLModel, table=True):
    __tablename__ = "draft_attachment_files"

    draft_attachment_file_id: uuid.UUID = Field(
        default_factory=uuid.uuid4, primary_key=True
    )

    draft_id: uuid.UUID = Field(foreign_key="drafts.draft_id", nullable=True)

    draft_attachment_id: uuid.UUID = Field(
        foreign_key="draft_attachments.draft_attachment_id", nullable=True
    )

    document_id: uuid.UUID = Field(foreign_key="documents.document_id", nullable=True)
