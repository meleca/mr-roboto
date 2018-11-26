"""Creates url_history table.

Revision ID: 56fab68d28b9
Revises: 754804413f2a
Create Date: 2018-11-20 11:46:09.340369
"""
from alembic import op
import sqlalchemy as sa
import datetime

revision = '56fab68d28b9'
down_revision = '754804413f2a'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'url_history',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('channel', sa.String(50), nullable=False),
        sa.Column('url', sa.String(200), nullable=False),
        sa.Column('title', sa.Unicode(200)),
        sa.Column('datetime', sa.DateTime, default=datetime.datetime.utcnow)
    )


def downgrade():
    op.drop_table('url_history')
