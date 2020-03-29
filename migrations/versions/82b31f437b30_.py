"""empty message

Revision ID: 82b31f437b30
Revises: e91038fb4a2d
Create Date: 2020-03-29 12:02:24.152596

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '82b31f437b30'
down_revision = 'e91038fb4a2d'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('users', 'username', new_column_name='name')


def downgrade():
    op.alter_column('users', 'name', new_column_name='username')
