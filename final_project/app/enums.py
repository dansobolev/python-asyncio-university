import enum
from typing import Dict


class UploadType(enum.Enum):
    PROFILE_IMAGE = 1
    COMMENT_ATTACHMENT_DOC = 2
    COMMENT_ATTACHMENT_IMAGE = 3

    __mapping__: Dict = {
        'PROFILE_IMAGE': 'Изображение в профиле пользователя',
        'COMMENT_ATTACHMENT_DOC': 'Вложение в комментарии (pdf документ)',
        'COMMENT_ATTACHMENT_IMAGE': 'Вложение в комментарии (изображение)',
    }
