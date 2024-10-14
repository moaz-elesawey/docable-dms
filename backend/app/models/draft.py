import uuid

from sqlmodel import Field, SQLModel


class Draft(SQLModel, table=True):
    __tablename__ = "drafts"

    draft_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    document_type_id: uuid.UUID = Field(
        foreign_key="document_types.document_type_id", nullable=True
    )

    structure_id: uuid.UUID = Field(
        foreign_key="structures.structure_id", nullable=True
    )

    document_id: uuid.UUID = Field(foreign_key="documents.document_id", nullable=True)
