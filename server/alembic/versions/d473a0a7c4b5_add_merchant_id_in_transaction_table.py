"""Add merchant_id in transaction table

Revision ID: d473a0a7c4b5
Revises: cf3d726b8e30
Create Date: 2023-04-30 23:09:33.850204

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd473a0a7c4b5'
down_revision = 'cf3d726b8e30'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transaction', sa.Column('merchant_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'transaction', 'merchant', ['merchant_id'], ['merchant_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'transaction', type_='foreignkey')
    op.drop_column('transaction', 'merchant_id')
    # ### end Alembic commands ###