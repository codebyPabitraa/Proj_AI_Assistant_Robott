"""add documents table
Revision ID: a757fa0a06a8
Revises: 8acf9a5f2662
Create Date: 2026-06-12 16:18:42.273371
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = 'a757fa0a06a8'
down_revision: Union[str, Sequence[str], None] = '8acf9a5f2662'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table('documents',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('filename', sa.String(length=255), nullable=False),
    sa.Column('file_type', sa.String(length=50), nullable=False),
    sa.Column('file_size', sa.Integer(), nullable=True),
    sa.Column('word_count', sa.Integer(), nullable=True),
    sa.Column('chunk_count', sa.Integer(), nullable=True),
    sa.Column('collection_name', sa.String(length=100), nullable=True),
    sa.Column('doc_id', sa.String(length=255), nullable=True),
    sa.Column('status', sa.String(length=50), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_documents_id'), 'documents', ['id'], unique=False)

def downgrade() -> None:
    op.drop_index(op.f('ix_documents_id'), table_name='documents')
    op.drop_table('documents')