from marshmallow import Schema, fields, EXCLUDE
from marshmallow_enum import EnumField

from app.auth.enums import SystemRoleEnum
from app.enums import UploadType


class UploadSchema(Schema):
    id = fields.UUID(required=True)
    created_at = fields.DateTime(format="%d.%m.%Y %H:%M:%S", dump_only=True)
    type = EnumField(UploadType)

    class Meta:
        additional = ('extension', 'fileName', 'file_size', 'file_mime_type')
        unknown = EXCLUDE


class UserSchema(Schema):
    id = fields.UUID(dump_only=True)
    login = fields.String(allow_none=False)
    email = fields.String(allow_none=False)
    phone_number = fields.String(allow_none=False)
    firstname = fields.String(allow_none=False)
    lastname = fields.String(allow_none=False)
    middlename = fields.String(allow_none=True)
    profile_image = fields.Nested(UploadSchema)
    role_type = EnumField(SystemRoleEnum, allow_none=False)
    is_banned = fields.Boolean(allow_none=False)


class DiscussionCommentSchema(Schema):
    id = fields.UUID(dump_only=True)
    created_at = fields.DateTime(format="%d.%m.%Y %H:%M:%S", dump_only=True)
    author = fields.Nested(UserSchema)
    author_id = fields.UUID(load_only=True)
    comment_text = fields.String(allow_none=False)
    attachments = fields.Nested(UploadSchema, many=True)
    replied_message = fields.Nested('DiscussionCommentSchema', allow_none=True)


class DiscussionSchema(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.String(allow_none=False)
    participants = fields.Nested(UserSchema, many=True)
    comments = fields.Nested(DiscussionCommentSchema, many=True)
