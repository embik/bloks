import os
import re
import markdown
from blog import app
from blog.models import Post
from unicodedata import normalize
from flask import Markup
from flask import render_template as flask_render_template

SLUG_REGEX = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')


def create_slug(title, delim='-'):
    '''
    Create a slug from a given title. Slugs are used to create a better browsing
    respectively linking experience for users and are save for use in URIs, e.g.
    /post/lorem-ipsum/ instead of /post/1.

    If a generated slug already exists, a numeric value is appended to the slug.
    This happens until a slug is greenlighted by check_slug().

    :param title: title of blog post
    :param delim: delimiter for finished slug (defaults to '-')
    :return: URI appropriate slug
    '''
    title = u'%s' % title
    result = []
    for token in SLUG_REGEX.split(title.lower()):
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
    '''
    Check a generated slug for prior existence. This is possible as blog post
    titles are not supposed to be unique and might be used two or more times.

    :param slug: slug to check
    :return: slug is greenlighted for use (true/false)
    '''
    if Post.query.filter_by(slug=slug).first():
        return False

    return True


def render_markdown(content):
    return Markup(markdown.markdown(content))


def render_template(template_name, **context):
    '''
    Render a template from a given name and context. In contrast to  flask's
    original render_template function this looks for the template file within
    the theme folder. This theme folder is configured in the BLOG_THEME
    configuration key.

    :param template_name: template to render
    :param context: given context for variables in template
    :return: rendered HTML output
    '''
    if 'BLOG_THEME' in app.config:
        return flask_render_template(os.path.join(app.config['BLOG_THEME'], template_name),
                                     **context)
    else:
        return flask_render_template(os.path.join('default', template_name), **context)


def allowed_file(filename):
    '''
    Check a filename for clearance to upload. Allowed filetype extensions are set
    in the configuration key UPLOAD_ALLOWED_EXTENSIONS.

    :param filename: filename to check for filetype
    :return: file is allowed for upload (true/false)
    '''
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['UPLOAD_ALLOWED_EXTENSIONS']
