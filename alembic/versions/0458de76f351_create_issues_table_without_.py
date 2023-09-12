"""Create issues table without relationships

Revision ID: 0458de76f351
Revises: 38c8687358b5
Create Date: 2023-09-10 20:11:47.267938

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0458de76f351'
down_revision = '38c8687358b5'
branch_labels = None
depends_on = None



def upgrade():
    op.create_table(
        'issues',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('content', sa.String, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('assigned_user_id', sa.Integer),
        sa.Column('project_id', sa.Integer)
    )

def downgrade():
    op.drop_table('issues')
