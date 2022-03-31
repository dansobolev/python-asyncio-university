import uuid
from typing import Optional, Union

from sqlalchemy import or_

from app.db import db
from app.db.models import User, Discussion, DiscussionParticipantRelation, \
    DiscussionComment, CommentAttachmentRelation
from app.exceptions import UserWithSuchLoginAlreadyExistedException, \
    UserNotFoundException, UserIsBannedException, DiscussionNotFound


async def get_user_by_login(login: str, raise_error: bool = False) -> Optional[User]:
    user = await User.query.where(User.login == login).gino.first()
    if not user and raise_error:
        raise UserNotFoundException
    return user


async def get_user_by_id(id_: Union[uuid.uuid4, str], raise_error: bool = False) -> Optional[User]:
    user = await User.get(id_)
    if not user and raise_error:
        raise UserNotFoundException
    return user


async def get_user_by_email(email: str, raise_error: bool = False) -> Optional[User]:
    user = await User.query.where(User.email == email).gino.first()
    if not user and raise_error:
        raise UserNotFoundException
    return user


async def check_user_uniqueness(login: str, email: str) -> Optional[User]:
    db_user = await User.query.where(
        or_(User.login == login, User.email == email)
    ).gino.first()
    return db_user


async def create_user(**kwargs):
    existed_user = await get_user_by_login(kwargs['login'])
    if existed_user:
        raise UserWithSuchLoginAlreadyExistedException
    db_user = User(**kwargs)
    await db_user.create()


async def is_valid_user(user: User) -> bool:
    if not user:
        raise UserNotFoundException

    if user.is_banned:
        raise UserIsBannedException

    return True


# TODO: create union class for query and loader
def base_discussion_query(uploads_profile, uploads_other):
    return db.select([(Discussion.
                       outerjoin(DiscussionParticipantRelation).
                       outerjoin(User, User.id == DiscussionParticipantRelation.participant_id).
                       outerjoin(DiscussionComment, Discussion.id == DiscussionComment.discussion_id).
                       outerjoin(uploads_profile,
                                 uploads_profile.id == User.profile_image_id).
                       outerjoin(CommentAttachmentRelation,
                                 CommentAttachmentRelation.comment_id == DiscussionComment.id).
                       outerjoin(uploads_other,
                                 uploads_other.id == CommentAttachmentRelation.upload_id))])


def base_discussion_loader(uploads_profile, uploads_other):
    loader = Discussion.distinct(Discussion.id) \
        .load(add_participant=User.distinct(User.id)
              .load(set_profile_image=uploads_profile.distinct(uploads_profile.id)),
              add_comment=DiscussionComment.distinct(DiscussionComment.id)
              .load(add_attachment=uploads_other.distinct(uploads_other.id), set_author=User))
    return loader


async def get_discussion_by_id(discussion_id: str) -> Discussion:
    discussion = await Discussion.get(discussion_id)
    if not discussion:
        raise DiscussionNotFound
    return discussion


async def get_user_discussion(discussion_id: str):
    query = Discussion.outerjoin(User).select().where(Discussion.id == discussion_id)
    query = await query.gino.load(Discussion.distinct(Discussion.id)
                                  .load(add_participant=User.distinct(User.id))).first()
    return query


async def is_user_discussion_participant(
        user_id: str,
        discussion: Union[Discussion, str]
) -> bool:
    if isinstance(discussion, Discussion):
        discussion_id = discussion.id
    else:
        discussion_id = discussion
    query = await get_user_discussion(discussion_id)
    if user_id not in [str(user.id) for user in query.participants]:
        print("User not in dialogue, Error!")
        raise
    return True
