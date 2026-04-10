"""change name admins table 

Revision ID: eb0736fb43be
Revises: 44affdf3e706
Create Date: 2026-04-10 17:33:04.956455

"""
# pylint: disable=no-member
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'eb0736fb43be'
down_revision: Union[str, Sequence[str], None] = '44affdf3e706'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('admins',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('first_name', sa.String(length=25), nullable=False),
    sa.Column('last_name', sa.String(length=25), nullable=False),
    sa.Column('username', sa.String(length=25), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('role', sa.String(length=20), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.drop_table('users')


def downgrade() -> None:
    """Downgrade schema."""
    op.create_table('users',
    sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('first_name', sa.VARCHAR(length=25), autoincrement=False, nullable=False),
    sa.Column('last_name', sa.VARCHAR(length=25), autoincrement=False, nullable=False),
    sa.Column('username', sa.VARCHAR(length=25), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('password', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('role', sa.VARCHAR(length=20), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('users_pkey')),
    sa.UniqueConstraint('email', name=op.f('users_email_key'), postgresql_include=[], postgresql_nulls_not_distinct=False),
    sa.UniqueConstraint('username', name=op.f('users_username_key'), postgresql_include=[], postgresql_nulls_not_distinct=False)
    )
    op.drop_table('admins')
