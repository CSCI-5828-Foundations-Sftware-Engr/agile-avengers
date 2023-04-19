"""Tables updated

Revision ID: 851fff3a6c23
Revises: 200dc919922c
Create Date: 2023-04-14 07:16:44.610623

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '851fff3a6c23'
down_revision = '200dc919922c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('debit_card', sa.Column('bank_account_number', sa.String(length=30), nullable=True))
    op.create_foreign_key(None, 'debit_card', 'bank_account', ['bank_account_number'], ['account_number'])
    op.add_column('transaction', sa.Column('transaction_method_id', sa.String(length=30), nullable=True))
    op.add_column('user_info', sa.Column('user_name', sa.String(length=30), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_info', 'user_name')
    op.drop_column('transaction', 'transaction_method_id')
    op.drop_constraint(None, 'debit_card', type_='foreignkey')
    op.drop_column('debit_card', 'bank_account_number')
    # ### end Alembic commands ###