"""empty message

Revision ID: 99b4716d2878
Revises: 
Create Date: 2020-08-29 09:29:58.780088

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '99b4716d2878'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sqlite_sequence')
    op.alter_column('references', 'Source',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('references', 'Target',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('references', 'Target',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('references', 'Source',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.create_table('sqlite_sequence',
    sa.Column('name', sa.NullType(), nullable=True),
    sa.Column('seq', sa.NullType(), nullable=True)
    )
    # ### end Alembic commands ###