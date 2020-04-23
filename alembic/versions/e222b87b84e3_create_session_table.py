"""create session table

Revision ID: e222b87b84e3
Revises: 61cc500cf3a8
Create Date: 2020-04-22 23:34:30.746140

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e222b87b84e3'
down_revision = '61cc500cf3a8'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'sessions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('ip_address', sa.String(), nullable=True),
        sa.Column('user_agent', sa.String(), nullable=False),
        sa.Column('last_accessed_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryConstraint('id')
    )

def downgrade():
    op.drop_table('sessions')
