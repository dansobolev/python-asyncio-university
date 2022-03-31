from dataclasses import dataclass, field
from typing import List, Dict
import os
import io

from aiohttp import web

from app.db.models import Upload, User, DiscussionComment
from app.config import Config
from app.enums import UploadType
from app.exceptions import UploadedFileTooLargeException, UploadNotFound


@dataclass
class UploadRestrictions:
    allowed_extensions: List[str] = field(default_factory=lambda: Config.UPLOAD_ALLOWED_EXTENSIONS)
    max_size: int = field(default=Config.UPLOAD_DEFAULT_MAX_LENGTH)


restrictions = {
    UploadType.PROFILE_IMAGE: UploadRestrictions(max_size=Config.UPLOAD_PROFILE_IMAGE_MAX_SIZE,
                                                 allowed_extensions=['png', 'jpg', 'jpeg'])
}


def get_upload_path(upload: Upload) -> str:
    return os.path.join(Config.UPLOAD_FOLDER_PATH, get_upload_name(upload))


def get_upload_name(upload: Upload) -> str:
    return f'{upload.id}.{upload.extension}'


def check_file_size(file: io.BufferedReader, max_size: int):
    file_length = get_size(file)
    if file_length > max_size:
        raise UploadedFileTooLargeException


def get_size(file: io.BufferedReader) -> int:
    pos = file.tell()
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(pos)
    return size


def validate_upload(file: web.FileField, upload_type: UploadType):
    upload_restrictions = restrictions[upload_type]

    allowed_extensions = upload_restrictions.allowed_extensions
    filename = file.filename

    extension = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''

    if not ('.' in filename and extension in allowed_extensions):
        # TODO: configure exception
        print('Invalid file or extension')

    max_size = upload_restrictions.max_size
    try:
        check_file_size(file.file, max_size)
    except UploadedFileTooLargeException:
        # TODO: configure exception
        print("Uploaded file is too large")


async def add_upload(file: web.FileField, upload_type: UploadType) -> Upload:
    upload = Upload(
        file_name=file.filename,
        type=upload_type,
        extension=file.filename.rsplit('.', 1)[1].lower(),
        file_size=get_size(file.file),
        file_mime_type=file.content_type or ''
    )
    upload = await upload.create()
    save_upload_file(file.file, upload)
    return upload


def save_upload_file(file: io.BufferedReader, upload: Upload):
    file_path = get_upload_path(upload)
    with open(file_path, 'wb') as file_:
        file_.write(file.read())


async def add_entity_attachment(entity, attachment: Dict) -> Upload:
    upload_id = attachment.get('upload_id')
    upload = await Upload.get(upload_id)
    if not upload:
        raise UploadNotFound

    if isinstance(entity, User):
        await entity.update(profile_image_id=upload.id).apply()
    elif isinstance(entity, DiscussionComment):
        await entity.comment_attachment_relation(upload_id=upload_id)
    else:
        print('Entity has no relationship with uploads')

    return upload


# TODO: type hints
async def add_entity_attachments(entity, attachments):
    for attachment in attachments:
        await add_entity_attachment(entity, attachment)
