import uuid
from datetime import datetime

from sqlmodel import Field, SQLModel


class _Mixin(SQLModel):
    """Generic Mixin"""


class _AuditableMixin(_Mixin):
    """
    Auditable Mixin Where it track creation, modification, and deletion of any object inherit form it.
    It also contains the `visible` attribute which indicated whether this record or instance
    is still existed or has been deleted.

    This `visible` attribute is very important as it what we will use to intercept the queries of SQLAlchemy
    and check if this record is valid to return in a `select` statement.
    """

    created_at: datetime | None = Field(default_factory=datetime.now, nullable=True)
    updated_at: datetime | None = Field(default_factory=datetime.now, nullable=True)
    deleted_at: datetime | None = Field(default_factory=datetime.now, nullable=True)

    created_by_id: uuid.UUID | None = Field(
        foreign_key="users.user_id", nullable=True, ondelete="SET NULL"
    )
    updated_by_id: uuid.UUID | None = Field(
        foreign_key="users.user_id", nullable=True, ondelete="SET NULL"
    )
    deleted_by_id: uuid.UUID | None = Field(
        foreign_key="users.user_id", nullable=True, ondelete="SET NULL"
    )

    visible: bool | None = Field(default=True, nullable=True)
