import os
import re
import markdown
from blog import app
from blog.models import Post
from unicodedata import normalize
from flask import Markup
from flask import render_template as flask_render_template

REGEX = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')


def create_slug(title, delim='-'):
    title = u'%s' % title
    result = []
    for token in REGEX.split(title.lower()):
        token = normalize('NFKD', token).encode('ascii', 'ignore')
        if token:
            result.append(token.decode('utf-8'))

    while check_slug(str(delim.join(result))) is False:
        try:
            result[len(result) - 1] = str(int(result[len(result) - 1]) + 1)
        except:
            result.append('1')

    return str(delim.join(result))


def check_slug(slug):
    if Post.query.filter_by(slug=slug).first():
        return False

    return True


def render_markdown(content):
    return Markup(markdown.markdown(content))


def render_template(template_file, **context):
    if 'BLOG_THEME' in app.config:
        return flask_render_template(os.path.join(app.config['BLOG_THEME'], template_file),
                                     **context)
    else:
        return flask_render_template(os.path.join('default', template_file), **context)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['UPLOAD_ALLOWED_EXTENSIONS']
