"""Add due_date to todos and create tags system

Revision ID: 003_add_due_date_and_tags
Revises: 002_add_users
Create Date: 2026-03-18 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "003_add_due_date_and_tags"
down_revision = "002_add_users"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add due_date column to todos table
    op.add_column("todos", sa.Column("due_date", sa.DateTime(), nullable=True))
    op.create_index("ix_todos_due_date", "todos", ["due_date"], unique=False)
    
    # Create tags table
    op.create_table(
        "tags",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("owner_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["owner_id"], ["users.id"]),
    )
    op.create_index("ix_tags_owner_id", "tags", ["owner_id"], unique=False)
    op.create_index("ix_tags_owner_id_name", "tags", ["owner_id", "name"], unique=True)
    
    # Create todos_tags junction table
    op.create_table(
        "todos_tags",
        sa.Column("todo_id", sa.Integer(), nullable=False),
        sa.Column("tag_id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("todo_id", "tag_id"),
        sa.ForeignKeyConstraint(["todo_id"], ["todos.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["tag_id"], ["tags.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_todos_tags_todo_id", "todos_tags", ["todo_id"], unique=False)
    op.create_index("ix_todos_tags_tag_id", "todos_tags", ["tag_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_todos_tags_tag_id", table_name="todos_tags")
    op.drop_index("ix_todos_tags_todo_id", table_name="todos_tags")
    op.drop_table("todos_tags")
    
    op.drop_index("ix_tags_owner_id_name", table_name="tags")
    op.drop_index("ix_tags_owner_id", table_name="tags")
    op.drop_table("tags")
    
    op.drop_index("ix_todos_due_date", table_name="todos")
    op.drop_column("todos", "due_date")
