import uuid

from sqlalchemy import func
from sqlalchemy.dialects.postgresql.base import UUID

from app.db import db
from app.auth.enums import SystemRoleEnum
from app.utils.custom_fields import IntEnum
from app.enums import UploadType


class TimestampMixin(db.Model):
    __abstract__ = True

    created_at = db.Column('created_at', db.DateTime, server_default=func.now(),
                           nullable=False, doc='Время создания объекта')
    updated_at = db.Column('updated_at', db.DateTime, server_default=func.now(),
                           onupdate=func.now(), nullable=False,
                           doc='Время обновления объекта')


class User(TimestampMixin):
    __tablename__ = 'users'

    id = db.Column('id', UUID(), primary_key=True, default=uuid.uuid4)
    login = db.Column('login', db.String, nullable=False)
    password = db.Column('password', db.LargeBinary, nullable=False)
    email = db.Column('email', db.String, nullable=False)
    phone_number = db.Column('phone_number', db.String, nullable=False)
    firstname = db.Column('firstname', db.String, nullable=False)
    lastname = db.Column('lastname', db.String, nullable=False)
    middlename = db.Column('middlename', db.String)
    profile_image_id = db.Column('profile_image_id', UUID(), db.ForeignKey('uploads.id'), nullable=True)
    role_type = db.Column('role_type', IntEnum(SystemRoleEnum), default=SystemRoleEnum.ORDINARY_USER)
    is_banned = db.Column('is_banned', db.Boolean, default=False)

    def __init__(self, **kw):
        super().__init__(**kw)
        self._discussions = set()
        self._profile_image = None

    @property
    def discussions(self):
        return self._discussions

    @discussions.setter
    def add_discussions(self, discussion):
        self._discussions.add(discussion)
        discussion.participants.add(self)

    @property
    def profile_image(self):
        return self._profile_image

    @profile_image.setter
    def set_profile_image(self, _profile_image):
        self._profile_image = _profile_image

    @property
    def fullname(self) -> str:
        return f'{self.lastname} {self.firstname}{" " + self.middlename if self.middlename else ""}'


class UserPasswordResetLink(TimestampMixin):
    __tablename__ = 'password_reset_links'

    id = db.Column('id', UUID(), primary_key=True, default=uuid.uuid4)
    user_id = db.Column('user_id', UUID(), db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    is_expired = db.Column('is_expired', db.Boolean, default=False)

    @property
    async def user(self):
        return await User.get(self.user_id)


class Discussion(TimestampMixin):
    __tablename__ = 'discussions'

    id = db.Column('id', UUID(), primary_key=True, default=uuid.uuid4)
    name = db.Column('name', db.String, nullable=False)
    creator_id = db.Column('creator_id', UUID(),
                           db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)

    def __init__(self, **kw):
        super().__init__(**kw)
        self._participants = set()
        self._comments = set()

    @property
    def participants(self):
        return self._participants

    @participants.setter
    def add_participant(self, participant):
        self._participants.add(participant)
        participant.discussions.add(self)

    @property
    def comments(self):
        return self._comments

    @comments.setter
    def add_comment(self, comment):
        self._comments.add(comment)

    @property
    async def creator(self):
        return await User.get(self.creator_id)

    async def discussion_participant_relation(self, participant_id: uuid.uuid4):
        await DiscussionParticipantRelation(discussion_id=self.id,
                                            participant_id=participant_id).create()


class DiscussionParticipantRelation(TimestampMixin):
    __tablename__ = 'discussions_participants_relation'

    discussion_id = db.Column('discussion_id', UUID(),
                              db.ForeignKey('discussions.id', ondelete="CASCADE"), nullable=False)
    participant_id = db.Column('participant_id', UUID(),
                               db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)


class DiscussionComment(TimestampMixin):
    __tablename__ = 'discussion_comments'

    id = db.Column('id', UUID(), primary_key=True, default=uuid.uuid4)
    author_id = db.Column('author_id', UUID(),
                          db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    discussion_id = db.Column('discussion_id', UUID(),
                              db.ForeignKey('discussions.id', ondelete="CASCADE"), nullable=False)
    comment_text = db.Column('comment_text', db.String, nullable=False)

    replied_message_id = db.Column('replied_message_id', UUID(),
                                   db.ForeignKey('discussion_comments.id', ondelete="CASCADE"),
                                   nullable=True, doc='Сообщение, на которое ответили данным сообщением')

    def __init__(self, **kw):
        super().__init__(**kw)
        self._attachments = set()
        self._author = None

    @property
    def author(self):
        return self._author

    @author.setter
    def set_author(self, _author):
        self._author = _author

    @property
    def attachments(self):
        return self._attachments

    @attachments.setter
    def add_attachment(self, attachment):
        self._attachments.add(attachment)

    async def comment_attachment_relation(self, upload_id: uuid.uuid4):
        await CommentAttachmentRelation(comment_id=self.id,
                                        upload_id=upload_id).create()


class CommentMentionRelation(TimestampMixin):
    __tablename__ = 'comments_mentions_relations'

    comment_id = db.Column('comment_id', UUID(),
                           db.ForeignKey('discussion_comments.id', ondelete="CASCADE"), nullable=False)
    author_id = db.Column('author_id', UUID(),
                          db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)


class CommentAttachmentRelation(TimestampMixin):
    __tablename__ = 'comments_attachments_relation'

    comment_id = db.Column('comment_id', UUID(),
                           db.ForeignKey('discussion_comments.id', ondelete="CASCADE"), nullable=False)
    upload_id = db.Column('upload_id', UUID(),
                          db.ForeignKey('uploads.id', ondelete="CASCADE"), nullable=False)


class Upload(TimestampMixin):
    __tablename__ = 'uploads'

    id = db.Column('id', UUID(), primary_key=True, default=uuid.uuid4)
    file_name = db.Column('file_name', db.String, nullable=False)
    type = db.Column('type', IntEnum(UploadType), nullable=False)
    extension = db.Column('extension', db.String, nullable=False)
    file_size = db.Column('file_size', db.Integer, server_default='0', nullable=False)
    file_mime_type = db.Column('file_mime_type', db.String)
