"""empty message

Revision ID: 4a3037741d2e
Revises: 
Create Date: 2021-11-15 22:19:01.482122

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4a3037741d2e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('todo',
    sa.Column('todo_No', sa.Integer(), nullable=False),
    sa.Column('todo_name', sa.String(length=255), nullable=True, comment='待办名称'),
    sa.Column('todo_desc', sa.String(length=255), nullable=True, comment='待办描述'),
    sa.Column('isfinish', sa.Integer(), nullable=True, comment='是否完成|0=未完成，1=已完成'),
    sa.Column('todo_date', sa.Date(), nullable=True, comment='截止时间'),
    sa.PrimaryKeyConstraint('todo_No')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('todo')
    # ### end Alembic commands ###
