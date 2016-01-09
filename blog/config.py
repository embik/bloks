import os
import base64

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'blog.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True

WTF_CSRF_ENABLED = True

SECRET_KEY = os.environ['BLOKS_SECRET_KEY'] if 'BLOKS_SECRET_KEY' in os.environ\
    else base64.b64encode(os.urandom(24))

LOG_PATH = os.environ['BLOKS_LOG_PATH'] if 'BLOKS_LOG_PATH' in os.environ\
    else os.path.join(basedir, 'tmp', 'blog.log')

BLOG_TITLE = 'example blog'
BLOG_DESCRIPTION = 'This is an example blog. It\'s authored by someone.'
BLOG_THEME = 'default'

POSTS_PER_PAGE = 5
ADMIN_POSTS_PER_PAGE = 20

UPLOAD_DIR = os.path.join(basedir, 'static', 'upload')
UPLOAD_DIR_URL = '/static/upload/'
UPLOAD_ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
