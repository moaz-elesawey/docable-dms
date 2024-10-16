import uuid

from sqlmodel import Session, func, select

from ..models.document_type import DocumentType, DocumentTypeCreate, DocumentTypeUpdate


def all(
    *, session: Session, skip: int = 0, limit: int = 100
) -> tuple[list[DocumentType], int]:
    """Retrive list of document types

    Args:
        session (Session): SQL Session
        skip (int, optional): number of document types to skip. Defaults to 0.
        limit (int, optional): number of document types to limit. Defaults to 100.

    Returns:
        tuple[list[DocumentType], int]: list of document types, and it's count
    """

    document_types = session.exec(select(DocumentType).offset(skip).limit(limit)).all()
    count = session.exec(select(func.count()).select_from(DocumentType)).one()

    return document_types, count


def create(
    *, session: Session, document_type_in: DocumentTypeCreate
) -> DocumentType | None:
    """Create a new instance of document type

    Args:
        session (Session): SQL Session
        document_type_in (DocumentTypeCreate): Document type data

    Returns:
        DocumentType | None
    """

    db_document_type = DocumentType.model_validate(document_type_in)

    try:
        session.add(db_document_type)
        session.commit()
        session.refresh(db_document_type, ["document_type_id"])
    except Exception as _e:
        session.rollback()
        return None

    return db_document_type


def retrive(*, session: Session, document_type_id: uuid.UUID) -> DocumentType | None:
    """Retrive a single document type or None

    Args:
        session (Session): SQL Session
        document_type_id (uuid.UUID): document type id

    Returns:
        DocumentType | None
    """

    db_document_type = session.exec(
        select(DocumentType).where(DocumentType.document_type_id == document_type_id)
    ).one_or_none()
    return db_document_type


def retrive_by_name(*, session: Session, name: str) -> DocumentType | None:
    """Retrive a single document type or None using it's name

    Args:
        session (Session): SQL Session
        name (str): name of document type

    Returns:
        DocumentType | None
    """

    db_document_type = session.exec(
        select(DocumentType).where(DocumentType.name == name)
    ).one_or_none()
    return db_document_type


def update(
    *,
    session: Session,
    db_document_type: DocumentType,
    document_type_in: DocumentTypeUpdate,
) -> DocumentType | None:
    """Update instance of document type

    Args:
        session (Session): SQL Session
        db_document_type (DocumentType): Database document type instance
        document_type_in (DocumentTypeUpdate): New data to update

    Returns:
        DocumentType | None
    """

    document_type_data = document_type_in.model_dump(exclude_unset=True)

    extra_data = {}

    db_document_type.sqlmodel_update(document_type_data, update=extra_data)

    try:
        session.add(db_document_type)
        session.commit()
        session.refresh(db_document_type)
    except Exception:
        session.rollback()
        return None

    return db_document_type


def delete(*, session: Session, db_document_type: DocumentType) -> bool:
    """Delete document type database instance

    Args:
        session (Session): SQL Session
        db_document_type (DocumentType): Database document type instance

    Returns:
        bool: whether instance deleted or not
    """

    try:
        session.delete(db_document_type)
        session.commit()
    except Exception:
        session.rollback()
        return False

    return True
