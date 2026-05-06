"""fix hashtags and add Outros catch-all category

Revision ID: 2f8c1a9e4b7d
Revises: 14eb944bc6c2
Create Date: 2026-05-06 00:00:00.000000

"""
# pylint: disable=no-member
from typing import Sequence, Union
from alembic import op


revision: str = '2f8c1a9e4b7d'
down_revision: Union[str, Sequence[str], None] = '14eb944bc6c2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Simplifica hashtags para palavras-chave curtas e adiciona categoria catch-all Outros."""
    op.execute("""
        UPDATE decorated_cakes SET hashtag = 'feminino',       updated_at = NOW() WHERE slug = 'feminino';
        UPDATE decorated_cakes SET hashtag = 'masculino',      updated_at = NOW() WHERE slug = 'masculino';
        UPDATE decorated_cakes SET hashtag = 'neutro',         updated_at = NOW() WHERE slug = 'neutro';
        UPDATE decorated_cakes SET hashtag = 'infantilmenina', updated_at = NOW() WHERE slug = 'infantil-menina';
        UPDATE decorated_cakes SET hashtag = 'infantilmenino', updated_at = NOW() WHERE slug = 'infantil-menino';
    """)

    op.execute("""
        INSERT INTO decorated_cakes (id, name, slug, hashtag, created_at, updated_at)
        VALUES (gen_random_uuid(), 'Outros', 'outros', 'outros', NOW(), NOW())
        ON CONFLICT (slug) DO NOTHING;
    """)


def downgrade() -> None:
    """Reverte hashtags para os valores originais e remove a categoria Outros."""
    op.execute("""
        UPDATE decorated_cakes SET hashtag = 'boloFeminino',       updated_at = NOW() WHERE slug = 'feminino';
        UPDATE decorated_cakes SET hashtag = 'boloMasculino',      updated_at = NOW() WHERE slug = 'masculino';
        UPDATE decorated_cakes SET hashtag = 'boloNeutro',         updated_at = NOW() WHERE slug = 'neutro';
        UPDATE decorated_cakes SET hashtag = 'boloInfantilMenina', updated_at = NOW() WHERE slug = 'infantil-menina';
        UPDATE decorated_cakes SET hashtag = 'boloInfantilMenino', updated_at = NOW() WHERE slug = 'infantil-menino';
    """)

    op.execute("DELETE FROM decorated_cakes WHERE slug = 'outros';")
