"""Initial migration

Revision ID: 4dd3002755fc
Revises: a3b67afe564d
Create Date: 2024-09-03 10:37:54.950990

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4dd3002755fc'
down_revision = 'a3b67afe564d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=20), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('image_file', sa.String(length=20), nullable=False),
    sa.Column('password', sa.String(length=60), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('dataset',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('date_uploaded', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('dataset')
    op.drop_table('user')
    # ### end Alembic commands ###
