"""add table instagram_posts

Revision ID: b83406813ee1
Revises: a081b98c66d6
Create Date: 2026-04-13 16:55:34.789574

"""
# pylint: disable=no-member
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = 'b83406813ee1'
down_revision: Union[str, Sequence[str], None] = 'a081b98c66d6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'instagram_posts',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('instagram_id', sa.String(length=100), nullable=False),
        sa.Column('caption', sa.String(length=2200), nullable=True),
        sa.Column('media_url', sa.String(length=500), nullable=False),
        sa.Column('permalink', sa.String(length=500), nullable=False),
        sa.Column('subcategory_id', sa.UUID(), nullable=True),
        sa.Column('is_featured', sa.Boolean(), nullable=False),
        sa.Column('featured_until', sa.DateTime(timezone=True), nullable=False),
        sa.Column('synced_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['subcategory_id'], ['decorated_cakes.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('instagram_id'),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('instagram_posts')
