"""add table product 

Revision ID: aea0e3d8bcbc
Revises: eb0736fb43be
Create Date: 2026-04-10 18:11:59.311662

"""
# pylint: disable=no-member
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'aea0e3d8bcbc'
down_revision: Union[str, Sequence[str], None] = 'eb0736fb43be'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('products',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('image_url', sa.String(length=500), nullable=True),
    sa.Column('category_id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('products')
