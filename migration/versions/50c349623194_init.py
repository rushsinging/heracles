"""init

Revision ID: 50c349623194
Revises: None
Create Date: 2013-07-27 13:03:32.967993

"""
from datetime import datetime

# revision identifiers, used by Alembic.
revision = '50c349623194'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'text',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('hashkey', sa.String(128), primary_key=True),
        sa.Column('parent_id', sa.Integer(),),
        sa.Column('content', sa.Unicode()),
        sa.Column('html', sa.Unicode()),
        sa.Column('content_type', sa.String(8))
    )

    op.create_table(
        'tag',
        sa.Column('title', sa.Unicode(32), primary_key=True)
    )

    op.create_table(
        'category',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.Unicode(32)))

    op.create_table(
        'blog',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.Unicode(128)),
        sa.Column('text_id', sa.Integer()),
        sa.Column('summary', sa.String(512)),
        sa.Column('category_id', sa.Integer()),
        sa.Column(
            'is_visible', sa.Boolean(),
            default=True, server_default='true'),
        sa.Column(
            'date_created', sa.DateTime(), default=datetime.now,
            server_default=sa.func.now()
        ),
        sa.Column(
            'date_modified', sa.DateTime(), default=datetime.now,
            server_default=sa.func.now()
        )
    )

    op.create_table(
        'blog_tags',
        sa.Column('blog_id', sa.Integer(), primary_key=True),
        sa.Column('tag', sa.Unicode(32), primary_key=True),)


def downgrade():
    op.drop_table('blog_tags')
    op.drop_table('blog')
    op.drop_table('category')
    op.drop_table('tag')
    op.drop_table('text')
