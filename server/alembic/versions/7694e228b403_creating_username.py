"""creating username

Revision ID: 7694e228b403
Revises: 7bea5b3be34b
Create Date: 2023-03-30 15:42:25.449945

"""
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func

from alembic import op

# revision identifiers, used by Alembic.
revision = '7694e228b403'
down_revision = '7bea5b3be34b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        Column("id", Integer, primary_key=True),
        Column("role", Integer, ForeignKey("role.id")),
        Column("username", String(64), nullable=False),
        Column("first_name", String(64), nullable=False),
        Column("last_name", String(64), nullable=False),
        Column("email_id", String(64), nullable=False),
        Column("updated_at", DateTime(timezone=True), nullable=False, default=func.now()),
        Column("updated_by", String(30), nullable=False),
        Column("created_at", DateTime(timezone=True), nullable=False),
        Column("created_by", String(30), nullable=False),
    )


def downgrade():
    op.drop_table("users")

