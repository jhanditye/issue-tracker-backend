"""create users table

Revision ID: 97d8c76499ca
Revises: 9f02599fda9f
Create Date: 2023-07-11 18:50:39.635766

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '97d8c76499ca'
down_revision = '9f02599fda9f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
    'users',
    sa.Column('id', sa.Integer(), nullable=False,primary_key=True),
    sa.Column('email', sa.String(), nullable=False, unique=True),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True),nullable=False, server_default=sa.text('now()'))
    )


def downgrade() -> None:
    op.drop_table("users")
