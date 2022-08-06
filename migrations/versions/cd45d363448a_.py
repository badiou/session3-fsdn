"""empty message

Revision ID: cd45d363448a
Revises: 0be6d79b6618
Create Date: 2022-08-06 19:06:14.184339

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cd45d363448a'
down_revision = '0be6d79b6618'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('etudiants', 'pays')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('etudiants', sa.Column('pays', sa.VARCHAR(length=200), autoincrement=False, nullable=True))
    # ### end Alembic commands ###