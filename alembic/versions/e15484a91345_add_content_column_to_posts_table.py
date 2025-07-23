"""add content column to posts table

Revision ID: e15484a91345
Revises: f95adab1821c
Create Date: 2023-10-19 12:41:33.920119

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e15484a91345'
down_revision: Union[str, None] = 'f95adab1821c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
