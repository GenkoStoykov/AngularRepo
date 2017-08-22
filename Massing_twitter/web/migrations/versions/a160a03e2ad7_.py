"""empty message

Revision ID: a160a03e2ad7
Revises: None
Create Date: 2017-08-19 21:24:10.135450

"""

# revision identifiers, used by Alembic.
revision = 'a160a03e2ad7'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=255), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('registered_on', sa.DateTime(), nullable=False),
    sa.Column('admin', sa.Boolean(), nullable=False),
    sa.Column('account_limit', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('accounts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('userid', sa.Integer(), nullable=False),
    sa.Column('fullname', sa.String(length=255), nullable=False),
    sa.Column('screenname', sa.String(length=255), nullable=False),
    sa.Column('description', sa.String(length=1024), nullable=False),
    sa.Column('avatar_url', sa.String(length=1024), nullable=False),
    sa.Column('followers', sa.Integer(), nullable=False),
    sa.Column('followings', sa.Integer(), nullable=False),
    sa.Column('oauth_token', sa.String(length=255), nullable=False),
    sa.Column('oauth_secret', sa.String(length=255), nullable=False),
    sa.Column('follow_schedule_status', sa.Boolean(), nullable=False),
    sa.Column('unfollow_schedule_status', sa.Boolean(), nullable=False),
    sa.Column('unfollow_schedule_option', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['userid'], [u'users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('follow_schedule',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('accountid', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.DateTime(), nullable=False),
    sa.Column('end_time', sa.DateTime(), nullable=False),
    sa.Column('max_follows', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['accountid'], [u'accounts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pools',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('accountid', sa.Integer(), nullable=False),
    sa.Column('added_on', sa.DateTime(), nullable=True),
    sa.Column('listname', sa.String(length=255), nullable=False),
    sa.Column('started_on', sa.DateTime(), nullable=True),
    sa.Column('progress', sa.Integer(), nullable=False),
    sa.Column('last_followed', sa.String(length=255), nullable=True),
    sa.Column('complete_status', sa.Boolean(), nullable=False),
    sa.Column('total_count', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['accountid'], [u'accounts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('unfollow_schedule',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('accountid', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.DateTime(), nullable=False),
    sa.Column('end_time', sa.DateTime(), nullable=False),
    sa.Column('max_unfollows', sa.Integer(), nullable=False),
    sa.Column('option', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['accountid'], [u'accounts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('followings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('poolid', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('status', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['poolid'], [u'pools.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('missfollowings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('poolid', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.ForeignKeyConstraint(['poolid'], [u'pools.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('missfollowings')
    op.drop_table('followings')
    op.drop_table('unfollow_schedule')
    op.drop_table('pools')
    op.drop_table('follow_schedule')
    op.drop_table('accounts')
    op.drop_table('users')
    ### end Alembic commands ###
