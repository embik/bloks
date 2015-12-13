import logging
from logging import Formatter
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.pagedown import PageDown

app = Flask(__name__)
app.config.from_object('blog.config')

assert 'BLOG_TITLE' in app.config, 'No BLOG_TITLE config value found'
assert 'BLOG_DESCRIPTION' in app.config, 'No BLOG_DESCRIPTION config value found'
assert 'SECRET_KEY' in app.config, 'No SECRET_KEY config value found'
assert 'LOG_PATH' in app.config, 'No LOG_PATH config value found'

# Initialize logging handler
handler = RotatingFileHandler(app.config['LOG_PATH'],
                              maxBytes=1000, backupCount=1)
handler.setFormatter(Formatter(
    '%(asctime)s %(levelname)s: %(message)s'
))
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)

# Initialize PageDown
pagedown = PageDown(app)

# Initialize SQLAlchemy database
db = SQLAlchemy(app)

# Initialize LoginManager
lm = LoginManager()
lm.init_app(app)

from blog import utils
app.jinja_env.globals.update(render_markdown=utils.render_markdown)

from blog import views, admin_views, errors, models
__all__ = ['views', 'admin_views', 'errors', 'models', ]
