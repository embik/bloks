from blog import app, lm, auth
from blog.forms import LoginForm
from blog.models import Post, User, Category
from blog.utils import render_theme_template
from flask import g, redirect, session, url_for, flash, abort
from flask.ext.login import current_user, login_required, logout_user
from sqlalchemy import desc


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user


@app.route('/')
@app.route('/index')
@app.route('/page/<int:id>')
def page(id=1):
    posts = Post.query.order_by(desc(Post.id)).\
        paginate(page=id, per_page=app.config['POSTS_PER_PAGE'])
    if posts:
        title = 'Page %d' % id if id > 1 else None
        categories = Category.query.all()
        return render_theme_template('page.html.j2', posts=posts, title=title,
                                     categories=categories)
    else:
        abort(404)


@app.route('/<string:slug>')
def post(slug):
    post = Post.query.filter_by(slug=slug).first()
    if post:
        return render_theme_template('post.html.j2', title=post.title, post=post)
    else:
        abort(404)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('page'))

    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return auth.try_login(form.username.data, form.password.data)

    return render_theme_template('login.html.j2', form=form, no_wrapper=True)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Successfuly signed out!')
    return redirect(url_for('login'))
