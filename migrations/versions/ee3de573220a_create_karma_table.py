"""Creates karma table.

Revision ID: ee3de573220a
Revises: e88a6b58cdc6
Create Date: 2018-12-10 19:17:38.312711
"""
from alembic import op
import sqlalchemy as sa

revision = 'ee3de573220a'
down_revision = 'e88a6b58cdc6'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'karma',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('channel', sa.String(50), nullable=False),
        sa.Column('entity', sa.String(50), nullable=False),
        sa.Column('status', sa.Integer, default=0)
    )


def downgrade():
    op.drop_table('karma')
