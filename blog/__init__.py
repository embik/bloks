from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.pagedown import PageDown

app = Flask(__name__)
app.config.from_object('blog.config')

assert 'BLOG_TITLE' in app.config, 'No BLOG_TITLE config value found'
assert 'BLOG_DESCRIPTION' in app.config, 'No BLOG_DESCRIPTION config value found'
assert 'SECRET_KEY' in app.config, 'No SECRET_KEY config value found'

pagedown = PageDown(app)
db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)

from blog import utils
app.jinja_env.globals.update(render_markdown=utils.render_markdown)

from blog import views, admin_views, errors, models
__all__ = ['views', 'admin_views', 'errors', 'models', ]
