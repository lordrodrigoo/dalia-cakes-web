"""add table decorated_cakes

Revision ID: a081b98c66d6
Revises: aea0e3d8bcbc
Create Date: 2026-04-13 16:21:01.967974

"""
# pylint: disable=no-member
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = 'a081b98c66d6'
down_revision: Union[str, Sequence[str], None] = 'aea0e3d8bcbc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'decorated_cakes',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('slug', sa.String(length=100), nullable=False),
        sa.Column('hashtag', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
        sa.UniqueConstraint('slug'),
        sa.UniqueConstraint('hashtag'),
    )

    op.execute("""
        INSERT INTO decorated_cakes (id, name, slug, hashtag, created_at, updated_at) VALUES
        (gen_random_uuid(), 'Feminino', 'feminino', 'boloFeminino', NOW(), NOW()),
        (gen_random_uuid(), 'Masculino', 'masculino', 'boloMasculino', NOW(), NOW()),
        (gen_random_uuid(), 'Neutro', 'neutro', 'boloNeutro', NOW(), NOW()),
        (gen_random_uuid(), 'Infantil Menina', 'infantil-menina', 'boloInfantilMenina', NOW(), NOW()),
        (gen_random_uuid(), 'Infantil Menino', 'infantil-menino', 'boloInfantilMenino', NOW(), NOW())
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('decorated_cakes')
