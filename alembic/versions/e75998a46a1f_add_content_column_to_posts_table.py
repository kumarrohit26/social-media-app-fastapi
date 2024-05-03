"""add content column to posts table

Revision ID: e75998a46a1f
Revises: 090c0cc8d6a6
Create Date: 2024-05-03 13:24:41.372136

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e75998a46a1f'
down_revision: Union[str, None] = '090c0cc8d6a6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
