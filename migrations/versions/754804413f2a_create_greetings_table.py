"""create greetings table

Revision ID: 754804413f2a
Revises: 
Create Date: 2018-11-19 17:26:26.139502

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '754804413f2a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'greetings',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('channel', sa.String(50), nullable=False),
        sa.Column('nick', sa.String(50), nullable=False),
        sa.Column('options', sa.Unicode(200)),
    )


def downgrade():
    op.drop_table('greetings')
