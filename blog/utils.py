import re
import markdown
from unicodedata import normalize
from blog.models import Post
from flask import Markup

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
