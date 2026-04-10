"""add categories table and change user to admin table 

Revision ID: 44affdf3e706
Revises: 5384aa5898d8
Create Date: 2026-04-10 17:30:19.767376

"""
# pylint: disable=no-member
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '44affdf3e706'
down_revision: Union[str, Sequence[str], None] = '5384aa5898d8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('categories',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('slug', sa.String(length=100), nullable=False),
    sa.Column('image_url', sa.String(length=500), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('slug')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('categories')
