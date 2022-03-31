# https://www.michaelcho.me/article/using-python-enums-in-sqlalchemy-models
import sqlalchemy as sa


class IntEnum(sa.types.TypeDecorator):
    """
    Enables passing in a Python enum and storing the enum's *value* in the db.
    The default would have stored the enum's *name* (ie the string).
    """
    impl = sa.Integer

    def __init__(self, enumtype, *args, **kwargs):
        super(IntEnum, self).__init__(*args, **kwargs)
        self._enumtype = enumtype

    @property
    def enum_type(self):
        return self._enumtype

    def process_bind_param(self, value, dialect):
        if isinstance(value, int):
            return value

        return value.value

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return self._enumtype(value)
