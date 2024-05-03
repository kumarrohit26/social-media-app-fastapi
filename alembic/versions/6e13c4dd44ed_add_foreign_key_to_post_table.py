"""add foreign key to post table

Revision ID: 6e13c4dd44ed
Revises: 1f1b6ef1b566
Create Date: 2024-05-03 15:56:14.552255

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6e13c4dd44ed'
down_revision: Union[str, None] = '1f1b6ef1b566'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fkey', source_table='posts', referent_table="users", local_cols=['user_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fkey', table_name='posts')
    op.drop_column('posts', 'user_id')
    pass
