import uuid

from sqlmodel import Session, func, select

from ..models.group import Group, GroupCreate, GroupUpdate


def all(
    *, session: Session, skip: int = 0, limit: int = 100
) -> tuple[list[Group], int]:
    """Retrive all groups from the database.

    Args:
        session (Session): SQL Database Session
        skip (int, optional): Groups count to skip (offset). Defaults to 0.
        limit (int, optional): Groups count to limit. Defaults to 100.

    Returns:
        list[Group], int
    """

    groups = session.exec(select(Group).offset(skip).limit(limit)).all()
    count = session.exec(select(func.count()).select_from(Group)).one()

    return groups, count


def create(*, session: Session, group_in: GroupCreate) -> Group | None:
    """Create User Object

    Args:
        session (Session): SQL Session DI
        group_in (GroupCreate): Create Group Data

    Returns:
        Group: Instance of Group
    """

    db_group = Group.model_validate(group_in)

    try:
        session.add(db_group)
        session.commit()
        session.refresh(db_group, ["group_id"])
    except Exception as _e:
        return None

    return db_group


def update(*, session: Session, db_group: Group, group_in: GroupUpdate) -> Group | None:
    """Update group instance data

    Args:
        session (Session): SQL Session DI
        db_group (Group): Database instance
        group_in (GroupUpdate): Group data

    Returns:
        Group | None: Updated database instance
    """

    group_data = group_in.model_dump(exclude_unset=True)

    extra_data = {}

    db_group.sqlmodel_update(group_data, update=extra_data)

    try:
        session.add(db_group)
        session.commit()
        session.refresh(db_group)
    except Exception:
        return None

    return db_group


def retrive(*, session: Session, group_id: uuid.UUID) -> Group | None:
    """Retrive group by it id

    Args:
        session (Session): SQL Session
        group_id (uuid.UUID): group id

    Returns:
        Group | None: Retrived group or None
    """

    group = session.get(Group, ident=group_id)
    return group


def retrive_by_name(*, session: Session, name: str) -> Group | None:
    """Retrive group by it's name

    Args:
        session (Session): SQL Session
        group_id (str): Group name

    Returns:
        Group | None: Retrived group or None
    """

    group = session.exec(select(Group).where(Group.name == name)).one_or_none()
    return group


def retrive_by_abbreviation(*, session: Session, abbreviation: str) -> Group | None:
    """Retrive group by it's abbreviation

    Args:
        session (Session): SQL Session
        group_id (str): Group abbreviation

    Returns:
        Group | None: Retrived group or None
    """

    group = session.exec(
        select(Group).where(Group.abbreviation == abbreviation)
    ).one_or_none()
    return group


def delete(*, session: Session, db_group: Group) -> bool:
    """Delete group from database

    Args:
        session (Session): SQL Session
        db_group (Group): Database instance of group

    Returns:
        bool: Wheather the group is deleted or None
    """

    try:
        session.delete(db_group)
        session.commit()
        return True
    except Exception as _e:
        return False
