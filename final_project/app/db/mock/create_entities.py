import random

from app.db.models import User, Discussion, DiscussionParticipantRelation, \
    DiscussionComment, CommentAttachmentRelation, Upload, CommentAttachmentRelation
from app.auth.enums import SystemRoleEnum
from app.db import db
from app.utils.password.hash import generate_hash
from app.enums import UploadType


logins = ['egor', 'oleg', 'zheka']
phones = ['123', '456', '789']
emails = ['123@gmail.com', '456@gmail.com', '789@gmail.com']
user_fields = ['login', 'password', 'email', 'phone_number',
               'firstname', 'lastname', 'middlename', 'role_type']


async def create_users():
    for _ in range(3):
        random_login = random.choice(logins)
        logins.remove(random_login)
        random_phone = random.choice(phones)
        phones.remove(random_phone)
        random_email = random.choice(emails)
        emails.remove(random_email)
        user = User(login=random_login,
                    password=generate_hash('test'),
                    email=random_email,
                    phone_number=random_phone,
                    firstname='firstname',
                    lastname='lastname',
                    role_type=SystemRoleEnum.ORDINARY_USER)
        await user.create()


async def create_discussion():
    creator = await User.query.where(User.login == 'egor').gino.first()
    discussion = Discussion(name='test_discussion', creator_id=creator.id)
    await discussion.create()

    # add participants (include creator)
    participant_creator = await User.query.where(User.login == 'egor').gino.first()
    await DiscussionParticipantRelation(discussion_id=discussion.id, participant_id=participant_creator.id).create()

    participant_1 = await User.query.where(User.login == 'oleg').gino.first()
    await DiscussionParticipantRelation(discussion_id=discussion.id, participant_id=participant_1.id).create()
    participant_2 = await User.query.where(User.login == 'zheka').gino.first()
    await DiscussionParticipantRelation(discussion_id=discussion.id, participant_id=participant_2.id).create()


async def main():
    db_uri = 'postgresql://danii:test@localhost/dansobolev'
    await db.set_bind(db_uri)
    """await create_users()
    await create_discussion()"""

    # delete all newly created mock data
    """await DiscussionParticipantRelation.delete.gino.all()

    discussions = await Discussion.query.gino.all()
    for discussion in discussions:
        await discussion.delete()

    users = await User.query.gino.all()
    for user in users:
        await user.delete()"""

    # TODO: loading queries
    """query = Discussion.outerjoin(DiscussionParticipantRelation).outerjoin(User).select()
    parents_loader = Discussion.distinct(Discussion.id).load(add_participant=User.distinct(User.id))
    parents = await query.gino.load(parents_loader).all()
    for parent in parents:
        print(f'Parent<{parent.id}> has {len(parent.participants)} children: {[c.id for c in parent.participants]}')"""

    user_id = '5f5eddf2-9a07-4ac6-84a0-8b3ca481141b'
    query = Discussion.outerjoin(DiscussionParticipantRelation).outerjoin(User) \
        .outerjoin(DiscussionComment).outerjoin(CommentAttachmentRelation).outerjoin(Upload).select()
    parents_loader = Discussion.distinct(Discussion.id)\
        .load(add_participant=User, add_comment=DiscussionComment.load(add_attachment=Upload))
    parent = await query.where(User.id == "5f5eddf2-9a07-4ac6-84a0-8b3ca481141b").\
        gino.load(parents_loader).all()
    print(parent)

    # TODO: test comment
    """await DiscussionComment(author_id='7d6e1a83-05ea-4d2b-b450-92bedaa23bd1',
                                      discussion_id='df0213d7-2f80-4001-97ca-a12ef86bc305',
                                      comment_text='text comment').create() """

    """upload = Upload(file_name='test',
                    type=UploadType.PROFILE_IMAGE,
                    extension='.jpg',
                    file_mime_type='image/jpg')
    upload = await upload.create()
    
    # comment_id: 8031e3a1-172f-4680-b65a-eb47d1f39b51
    
    relation = CommentAttachmentRelation(
        comment_id='8031e3a1-172f-4680-b65a-eb47d1f39b51',
        upload_id=upload.id
    )
    await relation.create()"""
