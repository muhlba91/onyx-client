"""Common list filters."""


def present(obj) -> bool:
    """Check if the object is not None.

    obj: the object to check"""
    return obj is not None
