#-*- coding: utf-8 -*-
from datetime import datetime
from hashlib import md5

import bs4

from bottle import cached_property
import sqlalchemy as sa

from share.framework.bottle.engines import db


def get_summary(content, content_type):
    if content_type == 'html':
        tmp = bs4.BeautifulSoup(content)
        p = tmp.find('p')
        if p:
            return p.text

        return ''


class TextModel(db.Model, db.TableOpt):
    __tablename__ = 'text'

    id = sa.Column(sa.Integer(), primary_key=True)
    hashkey = sa.Column(sa.String(128))
    parent_id = sa.Column(sa.Integer())
    content = sa.Column(sa.Unicode())
    html = sa.Column(sa.Unicode())
    content_type = sa.Column(sa.String(8))

    parent = db.relationship(
        'TextModel',
        uselist=False,
        primaryjoin='TextModel.parent_id == TextModel.id',
        foreign_keys='[TextModel.id]',
        remote_side='TextModel.parent_id'
    )


class BlogModel(db.Model, db.TableOpt):
    __tablename__ = 'blog'

    id = sa.Column(sa.Integer(), primary_key=True)
    title = sa.Column(sa.Unicode(128))
    text_id = sa.Column(sa.Integer())
    summary = sa.Column(sa.Unicode(512))
    date_created = sa.Column(
        sa.DateTime(), default=datetime.now,
        server_default=sa.func.now())
    date_modified = sa.Column(
        sa.DateTime(), default=datetime.now,
        server_default=sa.func.now())
    category_id = sa.Column(sa.Integer())
    is_visible = sa.Column(
        sa.Boolean(), default=True, server_default='true')

    text = db.relationship(
        'TextModel', backref='blog', uselist=False,
        primaryjoin='BlogModel.text_id == TextModel.id',
        foreign_keys='[BlogModel.text_id]',
    )
    tags = db.relationship(
        'TagModel',
        primaryjoin='BlogModel.id == BlogTagsModel.blog_id',
        secondary=lambda: BlogTagsModel.__table__,
        secondaryjoin='BlogTagsModel.tag == TagModel.title',
    )

    @cached_property
    def html(self):
        if self.text:
            return self.text.html
        return ''

    @cached_property
    def content(self):
        if self.text:
            return self.text.content
        return ''

    @cached_property
    def content_type(self):
        if self.text:
            return self.text.content_type
        return ''

    @classmethod
    def create(cls, title, content, content_type):
        t = TextModel()
        t.content = content
        if content_type == 'html':
            t.html = content

        t.hashkey = md5(t.html).hexdigest()
        t.content_type = content_type

        blog = BlogModel()
        blog.title = title
        blog.text = t
        blog.is_visible = True
        blog.summary = get_summary(content, content_type)
        return blog

    @classmethod
    def update(cls, blog_id, title, content, content_type):
        blog = cls.query.get(blog_id)
        if not blog:
            return

        html = ''
        if content_type == 'html':
            html = content
        hashkey = md5(html).hexdigest()
        if blog.text and hashkey == blog.text.hashkey:
            return blog

        t = TextModel(
            content=content, hashkey=hashkey, content_type=content_type,
        )
        if blog.text:
            t.parent_id = blog.text.id

        blog.text = t
        return blog


class CategoryModel(db.Model, db.TableOpt):
    __tablename__ = 'category'

    id = sa.Column(sa.Integer(), primary_key=True)
    title = sa.Column(sa.Unicode(32), nullable=False)


class BlogTagsModel(db.Model, db.TableOpt):
    __tablename__ = 'blog_tags'

    blog_id = sa.Column(
        sa.Integer(), primary_key=True)
    tag = sa.Column(sa.Unicode(32), primary_key=True)


class TagModel(db.Model, db.TableOpt):
    __tablename__ = 'tag'

    title = sa.Column(sa.Unicode(32), primary_key=True)
