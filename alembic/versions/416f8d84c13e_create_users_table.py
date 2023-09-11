"""Create users table

Revision ID: 416f8d84c13e
Revises: 
Create Date: 2023-09-10 20:09:24.234963

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '416f8d84c13e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String, unique=True, index=True, nullable=False),
        sa.Column('password', sa.String, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'))
    )

def downgrade():
    op.drop_table('users')