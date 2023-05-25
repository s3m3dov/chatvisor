"""Initial Migration

Revision ID: cd9e728914e4
Revises: 
Create Date: 2023-05-24 13:01:24.901024

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils
import pgvector



# revision identifiers, used by Alembic.
revision = 'cd9e728914e4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users_channels',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('platform', sa.Enum('TELEGRAM', 'DISCORD', name='platform'), nullable=False),
    sa.Column('platform_chat_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('prompt_messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(), nullable=True),
    sa.Column('channel_id', sa.Integer(), nullable=False),
    sa.Column('sender_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['channel_id'], ['users_channels.id'], ),
    sa.ForeignKeyConstraint(['sender_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('output_messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(), nullable=True),
    sa.Column('sender_id', sa.Enum('SYSTEM', 'GPT_3_5_TURBO', 'GPT_4', 'DALL_E', name='system_user'), nullable=False),
    sa.Column('prompt_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['prompt_id'], ['prompt_messages.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('output_messages')
    op.drop_table('prompt_messages')
    op.drop_table('users_channels')
    op.drop_table('users')
    # ### end Alembic commands ###
