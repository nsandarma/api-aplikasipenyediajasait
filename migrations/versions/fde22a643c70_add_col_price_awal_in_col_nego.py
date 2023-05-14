"""add col price awal in col nego

Revision ID: fde22a643c70
Revises: dfbd85909100
Create Date: 2023-05-14 23:16:56.055644

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fde22a643c70'
down_revision = 'dfbd85909100'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('nego', schema=None) as batch_op:
        batch_op.add_column(sa.Column('price_awal', sa.String(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('nego', schema=None) as batch_op:
        batch_op.drop_column('price_awal')

    # ### end Alembic commands ###