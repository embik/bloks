import os
import base64

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'blog.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True

WTF_CSRF_ENABLED = True

if 'BLOG_SECRET_KEY' in os.environ:
    SECRET_KEY = os.environ['BLOG_SECRET_KEY']
else:
    SECRET_KEY = base64.b64encode(os.urandom(24))

BLOG_TITLE = 'embik\'s blog'
BLOG_DESCRIPTION = 'no text'
POSTS_PER_PAGE = 5
