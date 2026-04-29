"""change media_url and permalink to text in instagram_posts

Revision ID: 3d1dbac93437
Revises: b83406813ee1
Create Date: 2026-04-29 17:06:49.114461

"""
# pylint: disable=no-member

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '3d1dbac93437'
down_revision: Union[str, Sequence[str], None] = 'b83406813ee1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column('instagram_posts', 'media_url',
               existing_type=sa.VARCHAR(length=500),
               type_=sa.Text(),
               existing_nullable=False)
    op.alter_column('instagram_posts', 'permalink',
               existing_type=sa.VARCHAR(length=500),
               type_=sa.Text(),
               existing_nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('instagram_posts', 'permalink',
               existing_type=sa.Text(),
               type_=sa.VARCHAR(length=500),
               existing_nullable=False)
    op.alter_column('instagram_posts', 'media_url',
               existing_type=sa.Text(),
               type_=sa.VARCHAR(length=500),
               existing_nullable=False)
