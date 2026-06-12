"""add hashed_password to users
Revision ID: 8acf9a5f2662
Revises: 7934c7f37e72
Create Date: 2026-06-12 12:53:18.887979
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '8acf9a5f2662'
down_revision: Union[str, Sequence[str], None] = '7934c7f37e72'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.add_column('users', sa.Column('hashed_password', sa.String(length=255), nullable=True))

def downgrade() -> None:
    op.drop_column('users', 'hashed_password')
