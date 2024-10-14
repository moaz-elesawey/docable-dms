import uuid

from sqlmodel import Field, SQLModel


class ChangeAssessment(SQLModel, table=True):
    __tablename__ = "change_assessments"

    change_assessment_id: uuid.UUID = Field(
        default_factory=uuid.uuid4, primary_key=True
    )

    document_id: uuid.UUID = Field(foreign_key="documents.document_id", nullable=True)

    revision_id: uuid.UUID = Field(foreign_key="revisions.revision_id", nullable=True)

    change_request_id: uuid.UUID = Field(
        foreign_key="change_requests.change_request_id", nullable=True
    )
