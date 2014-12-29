#-*- coding: utf-8 -*-
from bottle import redirect, url

from share.framework.bottle import MethodView, view
from share.framework.bottle import Pager
from share.framework.bottle import signin_required

from heracles.models import BlogModel


class BlogIndexView(MethodView):
    pager_limit = 5

    @view('blog/index.html')
    def get(self):
        query = BlogModel.query.filter(
            BlogModel.is_visible.is_(True)
        ).order_by(BlogModel.date_created.desc())

        pager = Pager(self)
        pager.set_total_count(query.count())

        return dict(blog_list=query.all(), pager=pager)


class BlogView(MethodView):
    @view('blog/blog.html')
    def get(self, blog_id):
        blog = BlogModel.query.get(blog_id)
        return dict(blog=blog)


class BlogEditView(MethodView):
    @view('blog/edit.html')
    @signin_required
    def get(self, blog_id):
        if blog_id:
            blog = BlogModel.query.get(blog_id)
        else:
            blog = BlogModel()

        return dict(blog=blog)

    def post(self, blog_id):
        if blog_id:
            blog = BlogModel.query.get(blog_id)
        else:
            blog = BlogModel()

        return redirect(url('heracles:www.blog', blog_id=blog.id))
