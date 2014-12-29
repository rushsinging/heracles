#-*- coding: utf-8 -*-
from share.framework.bottle.app import Blueprint

from .blog import BlogView, BlogIndexView
from .blog import BlogEditView

blueprint_www = Blueprint('www', subdomain='www')

blueprint_www.add_url_rule(
    '/<blog_id:int>/',
    view_func=BlogView.as_view(),
    methods=['GET'],
    endpoint='blog')
blueprint_www.add_url_rule(
    '/',
    view_func=BlogIndexView.as_view(),
    methods=['GET'],
    endpoint='index',
)
blueprint_www.add_url_rule(
    '/<blog_id:int>/edit/',
    view_func=BlogEditView.as_view(),
    methods=['GET', 'POST'],
    endpoint='blog_edit',
)
blueprint_www.add_url_rule(
    '/create/',
    view_func=BlogEditView.as_view(),
    methods=['GET', 'POST'],
    endpoint='blog_create',
    defaults={'blog_id': None}
)
