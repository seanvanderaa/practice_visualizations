"""Initial migration.

Revision ID: 867da8a0514e
Revises: 
Create Date: 2023-12-07 23:06:55.550848

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '867da8a0514e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('playlist_songs')
    with op.batch_alter_table('profiles', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('variance', sa.Float(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('profiles', schema=None) as batch_op:
        batch_op.drop_column('variance')
        batch_op.drop_column('user_id')

    op.create_table('playlist_songs',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('tempo', sa.FLOAT(), nullable=True),
    sa.Column('danceability', sa.FLOAT(), nullable=True),
    sa.Column('valence', sa.FLOAT(), nullable=True),
    sa.Column('loudness', sa.FLOAT(), nullable=True),
    sa.Column('energy', sa.FLOAT(), nullable=True),
    sa.Column('speechiness', sa.FLOAT(), nullable=True),
    sa.Column('acousticness', sa.FLOAT(), nullable=True),
    sa.Column('name', sa.VARCHAR(length=255), nullable=True),
    sa.Column('artist', sa.VARCHAR(length=255), nullable=True),
    sa.Column('album_cover', sa.VARCHAR(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###