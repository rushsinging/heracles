#-*- coding: utf-8 -*-
from datetime import datetime

from bottle import cached_property
import sqlalchemy as sa

from share.framework.bottle.engines import db


class TextModel(db.Model, db.TableOpt):
    __tablename__ = 'text'

    id = sa.Column(sa.Integer(), primary_key=True)
    hashkey = sa.Column(sa.String(128))
    parent_id = sa.Column(sa.Integer())
    content = sa.Column(sa.Unicode())
    html = sa.Column(sa.Unicode())

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
        foreign_keys='[BlogModel.text_id]'

    )
    tags = db.relationship(
        'TagModel',
        primaryjoin='BlogModel.id == BlogTagsModel.blog_id',
        secondary=lambda: BlogTagsModel.__table__,
        secondaryjoin='BlogTagsModel.tag == TagModel.title',
    )

    @cached_property
    def html(self):
        return self.text.html

    @cached_property
    def content(self):
        return self.text.content

    @staticmethod
    def create(content):
        return

    @staticmethod
    def update(blog_id, content):
        return


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
