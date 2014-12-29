#-*- coding: utf-8 -*-

import os
import hashlib
import re
from datetime import datetime

import bs4

from share.framework.bottle.restful import RESTfulAPI
from share.framework.bottle.engines import db
from share.utils.markdown import markdown

from heracles import app
from heracles.models import BlogModel, TextModel


class UpdateOpenAPI(RESTfulAPI):
    path = '/blog/update'
    methods = ['POST']

    def _get_title_summary(self, bs):
        title = bs.h1.text
        tmp = bs4.BeautifulSoup()

        h_num = 0
        for i in bs.contents:
            if re.match(ur'h\d', i.name or ''):
                h_num += 1

            if h_num >= 2:
                break

            tmp.append(i)

        return title, tmp.prettify()

    def _update_blogs(self, arg, directory, file_list):
        for file_name in file_list:
            blog = BlogModel.query.filter(
                BlogModel.file_name == file_name).first()
            md = open(os.path.join(directory, file_name), 'r').read()
            html = markdown(md)
            bs = bs4.BeautifulSoup(html)

            hashkey = hashlib.md5(md).hexdigest()

            if not blog:
                text = TextModel(
                    content=html, hashkey=hashkey, parent_hashkey=None)

                blog = BlogModel(file_name=file_name)
                db.session.add(text)
                db.session.add(blog)
            else:
                text = blog.text
                if text.hashkey == hashkey:
                    continue

                text = TextModel.query.get(hashkey)
                if not text:
                    text = TextModel(content=html, hashkey=hashkey)
                text.parent = blog.text
                blog.date_modified = datetime.now()

            blog.text = text
            # get_summary会影响get_title的结果, so 要先得到title
            blog.title, blog.summary = self._get_title_summary(bs)
            db.session.commit()

    def create(self):
        path = os.path.join(app.config['app_path'], 'templates/md')
        os.path.walk(path, self._update_blogs, None)
        return {}
