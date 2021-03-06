"""replied_message_id can be null

Revision ID: f9e2871666eb
Revises: 379b3b08c05d
Create Date: 2022-03-13 05:33:45.548770

"""
from alembic import op
import sqlalchemy as sa
import app.utils.custom_fields
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f9e2871666eb'
down_revision = '379b3b08c05d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('discussion_comments', 'replied_message_id',
               existing_type=postgresql.UUID(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('discussion_comments', 'replied_message_id',
               existing_type=postgresql.UUID(),
               nullable=False)
    # ### end Alembic commands ###
