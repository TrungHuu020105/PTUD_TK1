"""Initial migration - create todos table

Revision ID: 001_initial
Revises: None
Create Date: 2026-03-15 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision = "001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "todos",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(100), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("is_done", sa.Boolean(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_todos_title"), "todos", ["title"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_todos_title"), table_name="todos")
    op.drop_table("todos")
