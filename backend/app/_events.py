"""
Event listener for the sqlalchemy events
"""

from sqlalchemy import event

from .models.group import Group


def after_insert_event_listener(mapper, connection, target) -> None:
    """After insert event listener function

    Args:
        mapper (_type_): _description_
        connection (_type_): _description_
        target (_type_): _description_
    """

    print("INSERT")

    print(f"{mapper}: {type(mapper)}")
    print(f"{connection}: {type(connection)}")
    print(f"{target}: {type(target)}")


def after_update_event_listener(mapper, connection, target) -> None:
    """After update event listener function

    Args:
        mapper (_type_): _description_
        connection (_type_): _description_
        target (_type_): _description_
    """
    print("UPDATE")

    print(f"{mapper}: {type(mapper)}")
    print(f"{connection}: {type(connection)}")
    print(f"{target}: {type(target)}")


def after_delete_event_listener(mapper, connection, target) -> None:
    """After delete event listener function

    Args:
        mapper (_type_): _description_
        connection (_type_): _description_
        target (_type_): _description_
    """
    print("DELETE")

    print(f"{mapper}: {type(mapper)}")
    print(f"{connection}: {type(connection)}")
    print(f"{target}: {type(target)}")


def _register_sqlalchemy_event_listeners():
    """
    Register sqlalchemy event listener
    """

    # Insert Event Listener
    event.listen(Group, "after_insert", after_insert_event_listener)

    # Update Event Listener
    event.listen(Group, "after_update", after_update_event_listener)

    # Delete Event Listener
    event.listen(Group, "after_delete", after_delete_event_listener)
