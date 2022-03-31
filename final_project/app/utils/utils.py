from typing import List


def permissions_to_str(permissions: List) -> str:
    if not permissions:
        return ''
    permissions = ', '.join(permissions)
    return permissions


def permission_to_list(permissions: str) -> List:
    permissions = permissions.split(', ')
    return permissions
