"""Add users table and owner_id to todos

Revision ID: 002_add_users
Revises: 001_initial
Create Date: 2026-03-16 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "002_add_users"
down_revision = "001_initial"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="1"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    # Add owner_id column to todos table
    op.add_column("todos", sa.Column("owner_id", sa.Integer(), nullable=False, server_default="1"))
    op.create_index("ix_todos_owner_id", "todos", ["owner_id"], unique=False)
    
    # Add foreign key constraint
    op.create_foreign_key(
        "fk_todos_owner_id_users_id",
        "todos",
        "users",
        ["owner_id"],
        ["id"],
    )


def downgrade() -> None:
    op.drop_constraint("fk_todos_owner_id_users_id", "todos")
    op.drop_index("ix_todos_owner_id", table_name="todos")
    op.drop_column("todos", "owner_id")
    
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
