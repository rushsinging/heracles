#-*- coding: utf-8 -*-

from wtforms import Form, validators
from wtforms import StringField, SelectField


class BlogEditForm(Form):
    title = StringField(validators=[validators.Required()])
    content = StringField(validators=[validators.Required()])
    content_type = SelectField(
        choices=[('html', 'html'), ('md', 'md')])
