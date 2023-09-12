"""Create user-projects association table

Revision ID: 38c8687358b5
Revises: 4324660e1d6c
Create Date: 2023-09-10 20:11:10.687346

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '38c8687358b5'
down_revision = '4324660e1d6c'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'user_projects',
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
        sa.Column('project_id', sa.Integer, sa.ForeignKey('projects.id', ondelete='CASCADE'), primary_key=True)
    )

def downgrade():
    op.drop_table('user_projects')
