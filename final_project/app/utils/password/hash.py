from typing import Union
import bcrypt

from app.utils.password.exceptions import GeneratePasswordHashException, CheckPasswordHashException


def generate_hash(password_: Union[str, bytes]) -> bytes:
    try:
        return bcrypt.hashpw(
            password=password_.encode() if isinstance(password_, str) else password_,
            salt=bcrypt.gensalt(),
        )
    except (TypeError, ValueError) as error:
        raise GeneratePasswordHashException(str(error))


def check_hash(password_: str, hash_: bytes) -> None:
    try:
        result = bcrypt.checkpw(
            password=password_.encode(),
            hashed_password=hash_,
        )
    except (TypeError, ValueError) as error:
        raise CheckPasswordHashException(str(error))

    if not result:
        raise CheckPasswordHashException
