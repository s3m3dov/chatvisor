"""feat: add data column to UserChannel

Revision ID: 50622be69548
Revises: cd9e728914e4
Create Date: 2023-05-24 13:11:58.951905

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils
import pgvector



# revision identifiers, used by Alembic.
revision = '50622be69548'
down_revision = 'cd9e728914e4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users_channels', sa.Column('data', sa.JSON(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users_channels', 'data')
    # ### end Alembic commands ###
