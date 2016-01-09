from flask.ext.wtf import Form
from flask.ext.pagedown.fields import PageDownField
from wtforms import StringField, PasswordField, BooleanField, SelectField, FileField
from wtforms.validators import DataRequired


class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class PostForm(Form):
    title = StringField('title', validators=[DataRequired()])
    post = PageDownField('post', validators=[DataRequired()])
    category = SelectField('category', coerce=int)


class CategoryForm(Form):
    name = StringField('name', validators=[DataRequired()])
    image = FileField('image')


class UserForm(Form):
    nickname = StringField('nickname', validators=[DataRequired()])
    password = PasswordField('password')
    is_admin = BooleanField('is_admin', default=False)


class LinkForm(Form):
    label = StringField('label', validators=[DataRequired()])
    url = StringField('url', validators=[DataRequired()])


class RemovalForm(Form):
    is_confirmed = BooleanField('is_confirmed', default=False)
