import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response

from app import services as svc
from app.api.deps import SessionDep, get_current_active_superuser
from app.models.group import GroupCreate, GroupListPublic, GroupPublic, GroupUpdate

router = APIRouter()


@router.get(
    "/",
    response_model=GroupListPublic,
    dependencies=[
        Depends(get_current_active_superuser),
    ],
)
def read_groups(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """Read list of groups

    Args:
        session (SessionDep): SQL Database Session DI
        skip (int, optional): Groups count to skip (offset). Defaults to 0.
        limit (int, optional): Group count to limit. Defaults to 100.

    Returns:
        GroupListPublic: List of groups
    """

    groups, count = svc.group.all(session=session, skip=skip, limit=limit)
    return GroupListPublic(data=groups, count=count)


@router.get(
    "/{group_id}",
    response_model=GroupPublic,
    dependencies=[
        Depends(get_current_active_superuser),
    ],
)
def read_group(session: SessionDep, group_id: uuid.UUID) -> Any:
    """Read single group using it's id

    Args:
        session (SessionDep): SQL Database Session DI.
        group_id (uuid.UUID): Group ID.

    Returns:
        Group:

    Raises:
        HTTPException(404)
    """

    group = svc.group.retrive(session=session, group_id=group_id)

    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"success": False, "message": "Group not found"},
        )

    return group


@router.post(
    "/",
    response_model=GroupPublic,
    dependencies=[
        Depends(get_current_active_superuser),
    ],
    status_code=status.HTTP_201_CREATED,
)
def create_group(session: SessionDep, group_in: GroupCreate) -> Any:
    """Create a new instance of group.

    Args:
        session (SessionDep): SQL Database Session DI
        group_in (GroupCreate): Group Json data

    Returns:
        GroupPublic: created group

    Raises:
        HTTPException(500): if failed to save the group
        HTTPException(400): if group data already exists
    """

    if svc.group.retrive_by_name(session=session, name=group_in.name) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "success": False,
                "message": "group with this name already exists",
            },
        )

    if (
        svc.group.retrive_by_abbreviation(
            session=session, abbreviation=group_in.abbreviation
        )
        is not None
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "success": False,
                "message": "group with this abbreviation already exists",
            },
        )

    group = svc.group.create(session=session, group_in=group_in)

    if not group:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"success": False, "message": "something went wrong!"},
        )

    return group


@router.patch(
    "/{group_id}",
    dependencies=[Depends(get_current_active_superuser)],
    status_code=status.HTTP_202_ACCEPTED,
)
def update_group(
    *, session: SessionDep, group_id: uuid.UUID, group_in: GroupUpdate
) -> Any:
    """Update an existing group

    Args:
        session (SessionDep): SQL Database Session DI
        group_id (uuid.UUID): Group id
        group_in (GroupUpdate): Updatable data

    Returns:
        Group: if successed

    Raises:
        HTTPException(404): if the group id not found
        HTTPException(400): if the group data already exists
        HTTPException(500): if we failed to save the group
    """

    group = svc.group.retrive(session=session, group_id=group_id)

    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"success": False, "message": "Group not found"},
        )

    _group = svc.group.retrive_by_name(session=session, name=group_in.name)
    if _group and _group.group_id != group.group_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "success": False,
                "message": "group with this name already exists",
            },
        )

    _group = svc.group.retrive_by_abbreviation(
        session=session, abbreviation=group_in.abbreviation
    )
    if _group and _group.group_id != group.group_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "success": False,
                "message": "group with this abbreviation already exists",
            },
        )

    group = svc.group.update(session=session, db_group=group, group_in=group_in)

    if not group:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"success": False, "message": "something went wrong!"},
        )

    return group


@router.delete(
    "/{group_id}",
    dependencies=[Depends(get_current_active_superuser)],
)
def delete_group(*, session: SessionDep, group_id: uuid.UUID) -> Any:
    """Delete a group instance

    Args:
        session (SessionDep): SQL Database Session DI
        group_id (uuid.UUID): Group id

    Returns:
        Response(204)

    Raises:
        HTTPException(404): if the group does not exists
    """

    group = svc.group.retrive(session=session, group_id=group_id)

    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"success": False, "message": "Group not found"},
        )

    deleted = svc.group.delete(session=session, db_group=group)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"success": False, "message": "something went wrong!"},
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
