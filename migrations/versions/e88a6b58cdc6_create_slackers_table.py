"""Creates slackers table.

Revision ID: e88a6b58cdc6
Revises: 56fab68d28b9
Create Date: 2018-12-09 12:55:59.756464
"""
from alembic import op
import sqlalchemy as sa

revision = 'e88a6b58cdc6'
down_revision = '56fab68d28b9'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'slackers',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('channel', sa.String(50), nullable=False),
        sa.Column('nick', sa.String(50), nullable=False),
        sa.Column('words', sa.BigInteger, default=0)
    )


def downgrade():
    op.drop_table('slackers')
