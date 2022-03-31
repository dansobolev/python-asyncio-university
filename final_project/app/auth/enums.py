import enum
from typing import Dict


class SystemRoleEnum(enum.Enum):
    ORDINARY_USER = 1
    ADMIN = 3

    __mapping__: Dict = {
        'ORDINARY_USER': 'Пользователь',
        'ADMIN': 'Администратор'
    }
