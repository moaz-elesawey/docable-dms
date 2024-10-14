import uuid

from sqlmodel import Field, SQLModel


class Document(SQLModel, table=True):
    __tablename__ = "documents"

    document_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    document_type_id: uuid.UUID = Field(
        foreign_key="document_types.document_type_id", nullable=True
    )

    structure_id: uuid.UUID = Field(
        foreign_key="structures.structure_id", nullable=True
    )
