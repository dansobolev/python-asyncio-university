import enum
from typing import Dict, List, Optional
from functools import wraps
import json

from aiohttp_security import permits

from app.auth.enums import SystemRoleEnum
from app.db.queries import get_user_by_id, is_user_discussion_participant
from app.utils.utils import permissions_to_str


class AdminPermissions:
    PERM_MANAGE = 'PERM_MANAGE'
    PERM_MANAGE_GRANT_ACCESS = 'PERM_MANAGE_GRANT_ACCESS'


class ProjectPermissions:
    # general
    PERM_PROJECT = 'PERM_PROJECT'
    PERM_PROJECT_READ = 'PERM_PROJECT_READ'
    PERM_RPOJECT_UPDATE = 'PERM_PROJECT_CREATE'

    PERM_PROJECT_DISCUSSION_READ = 'PERM_PROJECT_DISCUSSION_READ'
    PERM_PROJECT_DISCUSSION_UPDATE = 'PERM_PROJECT_DISCUSSION_UPDATE'


project_permissions_map = {
    ProjectPermissions.PERM_PROJECT: [
        ProjectPermissions.PERM_PROJECT_READ,
        ProjectPermissions.PERM_RPOJECT_UPDATE
    ],
    ProjectPermissions.PERM_PROJECT_READ: [
        ProjectPermissions.PERM_PROJECT_DISCUSSION_READ
    ],
    ProjectPermissions.PERM_RPOJECT_UPDATE: [
        ProjectPermissions.PERM_RPOJECT_UPDATE
    ]
}


async def get_current_user_permissions(
        user_id: Optional[str],
        context: Optional[Dict]
) -> List[str]:
    if not user_id:
        return []
    user = await get_user_by_id(user_id)
    # TODO: ???
    if not user:
        return []
    discussion_id = context['discussion_id']
    permissions = []
    if user.role_type == SystemRoleEnum.ORDINARY_USER:
        permissions.extend([
            ProjectPermissions.PERM_PROJECT_DISCUSSION_READ,
        ])
        if discussion_id:
            if await is_user_discussion_participant(user.id, discussion_id):
                permissions.extend([
                    ProjectPermissions.PERM_PROJECT_DISCUSSION_UPDATE
                ])
    elif user.role_type == SystemRoleEnum.ADMIN:
        # TODO: permission for admin
        ...

    return [v for v in unpack_permissions(permissions, project_permissions_map)]


def permissions_required(permissions: List):
    def real_decorator(fn):
        @wraps(fn)
        async def wrapper(*args, **kwargs):
            request = args[-1]
            try:
                discussion_id = request.match_info.get('discussion_id') or \
                    (await request.json()).get('discussion_id')
            except json.decoder.JSONDecodeError:
                # if body is empty
                discussion_id = None
            await permits(request, permissions_to_str(permissions), context={'discussion_id': discussion_id})
            return await fn(*args, **kwargs)
        return wrapper
    return real_decorator


def unpack_permissions(
        permissions: List[str],
        perm_map: Dict[str, List[str]]
) -> List[str]:
    res = []
    for perm in permissions:
        child_perms = perm_map.get(perm)
        if child_perms:
            permissions.extend(child_perms)
        else:
            res.append(perm)
    return list(set(res))
