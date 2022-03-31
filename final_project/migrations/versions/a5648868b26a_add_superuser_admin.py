"""add superuser (admin)

Revision ID: a5648868b26a
Revises: 5a02b7d10c2a
Create Date: 2022-03-09 02:59:30.691901

"""
import uuid

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from app.auth.enums import SystemRoleEnum
from app.config import Config
from app.utils.custom_fields import IntEnum
from app.utils.password.hash import generate_hash


# revision identifiers, used by Alembic.
revision = 'a5648868b26a'
down_revision = '5a02b7d10c2a'
branch_labels = None
depends_on = None

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    login = sa.Column('login', sa.String, nullable=False)
    password = sa.Column('password', sa.LargeBinary, nullable=False)
    email = sa.Column('email', sa.String, nullable=False)
    phone_number = sa.Column('phone_number', sa.String, nullable=False)
    firstname = sa.Column('firstname', sa.String, nullable=False)
    lastname = sa.Column('lastname', sa.String, nullable=False)
    middlename = sa.Column('middlename', sa.String)
    role_type = sa.Column('role_type', IntEnum(SystemRoleEnum), default=SystemRoleEnum.ORDINARY_USER)


def upgrade():
    session = Session(bind=op.get_bind())
    existed_admin = session.query(User).filter(User.login == 'admin').first()
    if existed_admin:
        return
    admin_data = {'login': 'admin', 'password': generate_hash(Config.ADMIN_PASSWORD),
                  'email': Config.ADMIN_EMAIL, 'phone_number': Config.ADMIN_PHONE_NUMBER,
                  'firstname': 'admin', 'lastname': 'adminov', 'middlename': 'adminovich',
                  'role_type': SystemRoleEnum.ADMIN}
    admin = User(**admin_data)
    session.add(admin)
    session.commit()


def downgrade():
    pass
