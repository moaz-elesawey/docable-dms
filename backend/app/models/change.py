import uuid

from sqlmodel import Field, SQLModel


class Change(SQLModel, table=True):
    __tablename__ = "changes"

    change_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    document_id: uuid.UUID = Field(foreign_key="documents.document_id", nullable=True)

    old_revision_id: uuid.UUID = Field(
        foreign_key="revisions.revision_id", nullable=True
    )

    change_request_id: uuid.UUID = Field(
        foreign_key="change_requests.change_request_id", nullable=True
    )

    change_assessment_id: uuid.UUID = Field(
        foreign_key="change_assessments.change_assessment_id", nullable=True
    )

    change_acceptance_id: uuid.UUID = Field(
        foreign_key="change_acceptances.change_acceptance_id", nullable=True
    )

    new_revision_id: uuid.UUID = Field(
        foreign_key="revisions.revision_id", nullable=True
    )
