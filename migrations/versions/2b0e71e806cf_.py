"""empty message

Revision ID: 2b0e71e806cf
Revises: 
Create Date: 2022-05-08 12:05:14.727409

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2b0e71e806cf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('teachers', sa.Column('salary', sa.Numeric(precision=10, scale=2), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('teachers', 'salary')
    # ### end Alembic commands ###
