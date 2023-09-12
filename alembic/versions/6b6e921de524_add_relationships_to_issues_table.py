"""Add relationships to issues table

Revision ID: 6b6e921de524
Revises: 0458de76f351
Create Date: 2023-09-10 20:12:23.562580

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6b6e921de524'
down_revision = '0458de76f351'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('issues') as batch_op:
        batch_op.create_foreign_key(
            "fk_issues_assigned_user", 
            "users", 
            ["assigned_user_id"], 
            ["id"], 
            ondelete="CASCADE"
        )
        batch_op.create_foreign_key(
            "fk_issues_project", 
            "projects", 
            ["project_id"], 
            ["id"], 
            ondelete="CASCADE"
        )

def downgrade():
    with op.batch_alter_table('issues') as batch_op:
        batch_op.drop_constraint("fk_issues_assigned_user", type_="foreignkey")
        batch_op.drop_constraint("fk_issues_project", type_="foreignkey")
