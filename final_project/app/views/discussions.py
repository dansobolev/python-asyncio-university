from aiohttp import web
from aiohttp_security import authorized_userid
from marshmallow import EXCLUDE

from app.auth.permissions import permissions_required, ProjectPermissions
from app.db import db
from app.db.queries import is_user_discussion_participant, base_discussion_query,\
    base_discussion_loader, get_discussion_by_id, get_user_discussion
from app.db.models import Discussion, DiscussionParticipantRelation, Upload, DiscussionComment, User
from app.utils.validation import DiscussionSchema, DiscussionCommentSchema
from app.uploads import add_entity_attachments

routes = web.RouteTableDef()


@routes.post('/discussions')
async def create_discussion(request: web.Request) -> web.Response:
    """user_id = await authorized_userid(request)
    if not user_id:
        raise web.HTTPUnauthorized"""
    # for testing purposes
    user_id = '73c96ff9-ab5f-4e07-b94e-e8bf8c9dce82'
    data = await request.json()
    validated_data = DiscussionSchema(only=('name',), unknown=EXCLUDE).load(data)
    validated_data.update({'creator_id': user_id})
    discussion = await Discussion(**validated_data).create()
    await discussion.discussion_participant_relation(participant_id=user_id)
    return web.json_response(DiscussionSchema().dump(await get_user_discussion(discussion.id)))


# TODO: pass {user_id} to parameter query on front and parse it here to get user
#  rename to something like /{user-id}/discussions/list
@routes.get('/discussions/list', name='user-discussions')
@permissions_required(permissions=[ProjectPermissions.PERM_PROJECT_DISCUSSION_READ])
async def get_user_discussions(request: web.Request) -> web.Response:
    user_id = await authorized_userid(request)
    if not user_id:
        raise web.HTTPUnauthorized
    # user_id = '73c96ff9-ab5f-4e07-b94e-e8bf8c9dce82'

    user_discussions = db.select([
        Discussion.id
    ]).select_from(
        Discussion.outerjoin(DiscussionParticipantRelation)
    ).where(
        DiscussionParticipantRelation.participant_id == user_id
    )

    uploads_profile = Upload.alias('uploads_profile')
    uploads_other = Upload.alias('uploads_other')

    base_query = base_discussion_query(uploads_profile, uploads_other)
    query = base_query.where(Discussion.id.in_(user_discussions))

    loader = base_discussion_loader(uploads_profile, uploads_other)
    discussions = await query. \
        gino.load(loader).all()

    answer = DiscussionSchema(many=True).dump(discussions)

    return web.json_response(answer)


# TODO: rename to /discussions/list
@routes.get('/all-discussions/list', name='all-discussions')
async def get_all_discussion(request: web.Request) -> web.Response:
    uploads_profile = Upload.alias('uploads_profile')
    uploads_other = Upload.alias('uploads_other')

    query = base_discussion_query(uploads_profile, uploads_other)
    loader = base_discussion_loader(uploads_profile, uploads_other)
    discussions = await query. \
        gino.load(loader).all()
    answer = DiscussionSchema(many=True).dump(discussions)

    return web.json_response(answer)


@routes.post('/{discussion_id}/comments')
@permissions_required(permissions=[ProjectPermissions.PERM_PROJECT_DISCUSSION_UPDATE])
async def create_discussion_comment(request: web.Request) -> web.Response:
    """user_id = await authorized_userid(request)
        if not user_id:
            raise web.HTTPUnauthorized"""
    user_id = '73c96ff9-ab5f-4e07-b94e-e8bf8c9dce82'
    discussion_id = request.match_info['discussion_id']
    discussion = await get_discussion_by_id(discussion_id)
    # проверка на то что пользователь состоит в диалоге
    await is_user_discussion_participant(user_id, discussion)

    comment_data = await request.json()
    validated_data = DiscussionCommentSchema(unknown=EXCLUDE).load(comment_data)
    validated_data.update({'discussion_id': discussion.id})
    discussion_comment = await DiscussionComment(**validated_data).create()

    if 'attachments' in validated_data:
        attachments = validated_data.pop('attachments')
        await add_entity_attachments(discussion_comment, attachments)

    return web.json_response(DiscussionCommentSchema().dump(discussion_comment))
