import uuid

from sqlmodel import Field, SQLModel


class Structure(SQLModel, table=True):
    __tablename__ = "structures"

    structure_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
