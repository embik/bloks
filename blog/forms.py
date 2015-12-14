from flask.ext.wtf import Form
from flask.ext.pagedown.fields import PageDownField
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired


class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class PostForm(Form):
    title = StringField('title', validators=[DataRequired()])
    post = PageDownField('post', validators=[DataRequired()])


class CategoryForm(Form):
    name = StringField('name', validators=[DataRequired()])
    image_url = StringField('image_url')


class UserForm(Form):
    nickname = StringField('nickname', validators=[DataRequired()])
    password = PasswordField('password')
    is_admin = BooleanField('is_admin', default=False)


class RemovalForm(Form):
    is_confirmed = BooleanField('is_confirmed', default=False)
