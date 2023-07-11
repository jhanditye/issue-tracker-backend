"""create issues table

Revision ID: 9f02599fda9f
Revises: 
Create Date: 2023-07-11 18:33:20.839658

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f02599fda9f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
    'issues',
    sa.Column('id', sa.Integer(), nullable=False,primary_key=True),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('content', sa.String(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True),nullable=False, server_default=sa.text('now()'))
    )


def downgrade() -> None:
    op.drop_table("issues")
