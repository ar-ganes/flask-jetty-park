"""Add new fields to blacklist_entries

Revision ID: e0643067a8fe
Revises: 2b719a67ab1a
Create Date: 2024-12-23 15:17:40.317682

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e0643067a8fe'
down_revision = '2b719a67ab1a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('blacklist_entries', schema=None) as batch_op:
        batch_op.add_column(sa.Column('license_plate', sa.String(length=20), nullable=False))
        batch_op.add_column(sa.Column('make_model', sa.String(length=100), nullable=False))
        batch_op.add_column(sa.Column('individual_name', sa.String(length=100), nullable=False))
        batch_op.add_column(sa.Column('blacklisted_date', sa.Date(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('blacklist_entries', schema=None) as batch_op:
        batch_op.drop_column('blacklisted_date')
        batch_op.drop_column('individual_name')
        batch_op.drop_column('make_model')
        batch_op.drop_column('license_plate')

    # ### end Alembic commands ###
