#-*- coding: utf-8 -*-
from share.utils.decorators import content2html
from share.framework.bottle import default_app
from share.framework.bottle import MethodView, view
from share.framework.bottle import NotFound
from share.framework.bottle import Pager

from heracles.models import BlogModel


class BlogEditView(MethodView):
    @view('blog/edit.html')
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
