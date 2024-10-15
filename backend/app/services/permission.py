import uuid

from sqlmodel import Session, func, select

from ..models.permission import Permission, PermissionCreate, PermissionUpdate


def all(
    *,
    session: Session,
    skip: int = 0,
    limit: int = 0,
) -> tuple[list[Permission], int]:
    """Get all permission from the database

    Args:
        session (Session): SQL Session DI
        skip (int, optional): number of permissions to skip (offset). Defaults to 0.
        limit (int, optional): number of permissions to limit. Defaults to 0.

    Returns:
        tuple[list[Permission], int]
    """

    permissions = session.exec(select(Permission).offset(skip).limit(limit)).all()
    count = session.exec(select(func.count()).select_from(Permission)).one_or_none()

    return permissions, count


def create(*, session: Session, permission_in: PermissionCreate) -> Permission | None:
    """Create and save a new permission

    Args:
        session (Session): SQL Session
        permission_in (PermissionCreate): permission data

    Returns:
        Permission | None
    """

    db_permission = Permission.model_validate(permission_in)

    try:
        session.add(db_permission)
        session.commit()
        session.refresh(db_permission, ["permission_id"])
    except Exception:
        session.rollback()
        return None

    return db_permission


def retrive(*, session: Session, permission_id: uuid.UUID) -> Permission | None:
    """Retrive permission by id

    Args:
        session (Session): SQL Session
        permission_id (uuid.UUID): permission id

    Returns:
        Permission | None
    """

    permission = session.get(Permission, ident=permission_id)
    return permission


def retrive_by_name(*, session: Session, name: str) -> Permission | None:
    """Retrive permission by name

    Args:
        session (Session): SQL Session
        name (str): Permission name

    Returns:
        Permission | None
    """

    permission = session.exec(
        select(Permission).where(Permission.name == name)
    ).one_or_none()
    return permission


def retrive_by_codename(*, session: Session, codename: str) -> Permission | None:
    """Retrive permission by codename

    Args:
        session (Session): SQL Session
        codename (str): Permission codename

    Returns:
        Permission | None
    """

    permission = session.exec(
        select(Permission).where(Permission.codename == codename)
    ).one_or_none()
    return permission


def update(
    *, session: Session, db_permission: Permission, permission_in: PermissionUpdate
) -> Permission | None:
    """Update permission instance

    Args:
        session (Session): SQL Session
        db_permission (Permission): Database permission instance
        permission_in (PermissionUpdate): New permission data

    Returns:
        Permission | None
    """

    permission_data = permission_in.model_dump(exclude_unset=True)

    extra_data = {}

    db_permission.sqlmodel_update(permission_data, update=extra_data)

    try:
        session.add(db_permission)
        session.commit()
        session.refresh(db_permission)
    except Exception as _e:
        session.rollback()
        return None

    return db_permission


def delete(*, session: Session, db_permission: Permission) -> bool:
    """Delete permission instance

    Args:
        session (Session): SQL Session
        db_permission (Permission): Database permission instance

    Returns:
        bool: whether deleted or not
    """

    try:
        session.delete(db_permission)
        session.commit()
    except Exception as _e:
        session.rollback()
        return False

    return True
