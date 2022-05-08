"""empty message

Revision ID: aadd1d9c6b5a
Revises: 67401b87d112
Create Date: 2022-05-08 14:47:18.043963

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aadd1d9c6b5a'
down_revision = '67401b87d112'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('students', sa.Column('results', sa.Numeric(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('students', 'results')
    # ### end Alembic commands ###
