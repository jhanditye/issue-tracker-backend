"""Create projects table

Revision ID: 4324660e1d6c
Revises: 416f8d84c13e
Create Date: 2023-09-10 20:10:16.768401

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4324660e1d6c'
down_revision = '416f8d84c13e'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'projects',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('description', sa.String, nullable=False)
    )

def downgrade():
    op.drop_table('projects')
