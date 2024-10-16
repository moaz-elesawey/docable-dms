import uuid

from sqlalchemy import Text
from sqlmodel import Field, SQLModel

from ._mixins import _AuditableMixin


class DocumentTypeBase(_AuditableMixin, SQLModel):
    name: str = Field(max_length=255, nullable=False, unique=True, index=True)
    abbreviation: str = Field(max_length=255, nullable=False, unique=True, index=True)
    description: str | None = Field(
        max_length=255, nullable=True, sa_type=Text(), default="N/A"
    )


class DocumentTypeCreate(DocumentTypeBase):
    pass


class DocumentTypeUpdate(DocumentTypeBase):
    name: str | None = Field(default=None, max_length=255)
    abbreviation: str | None = Field(default=None, max_length=255)
    description: str | None = Field(default=None)


class DocumentType(DocumentTypeBase, table=True):
    __tablename__ = "document_types"

    document_type_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


class DocumentTypePublic(DocumentTypeBase):
    document_type_id: uuid.UUID


class DocumentTypeListPublic(SQLModel):
    data: list[DocumentTypePublic]
    count: int
