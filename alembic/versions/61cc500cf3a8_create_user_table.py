"""create user table

Revision ID: 61cc500cf3a8
Revises: 
Create Date: 2020-04-22 23:34:21.020824

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '61cc500cf3a8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('first_name', sa.String(), nullable=True),
        sa.Column('last_name', sa.String(), nullable=True),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('is_superuser', sa.Boolean(), nullable=True),
        sa.PrimaryConstraint('id')
    )
    op.create_index(of.f('idx_user_email'), 'users', ['email'], unique=True)

def downgrade():
    op.drop_index(op.f('idx_user_email'), table_name='users')
    op.drop_table('users')
