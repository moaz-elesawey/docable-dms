import uuid

from sqlmodel import Field, SQLModel


class DocumentType(SQLModel, table=True):
    __tablename__ = "document_types"

    document_type_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
