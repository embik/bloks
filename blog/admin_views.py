from blog import app, db
from blog.forms import PostForm
from blog.models import Post, User, Category
from blog.utils import create_slug
from flask import render_template, flash, url_for, redirect, abort
from flask.ext.login import login_required, current_user
from datetime import datetime
from sqlalchemy import desc


@app.route('/admin/dashboard')
@app.route('/admin/dashboard/<int:id>')
@login_required
def admin_dashboard(id=1):
    posts = Post.query.order_by(desc(Post.id)).\
        paginate(page=id, per_page=app.config['ADMIN_POSTS_PER_PAGE'])
    users = User.query.all()
    categories = Category.query.all()
    return render_template('admin/dashboard.html.j2', posts=posts, users=users,
                           categories=categories, title='Dashboard')


@app.route('/admin/users/new', methods=['POST', 'GET'])
@login_required
def new_user():
    return ''


@app.route('/admin/users/edit/<int:id>', methods=['POST', 'GET'])
@login_required
def edit_user(id):
    return ''


@app.route('/admin/categories/new', methods=['POST', 'GET'])
@login_required
def new_category():
    return ''


@app.route('/admin/categories/edit/<int:id>', methods=['POST', 'GET'])
@login_required
def edit_category(id):
    return ''


@app.route('/admin/posts/new', methods=['POST', 'GET'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.post.data, timestamp=datetime.utcnow(),
                    slug=create_slug(form.title.data), user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live! <a href="%s">Click here</a>'
              % url_for('post', slug=post.slug))
        return redirect(url_for('page'))
    else:
        return render_template('admin/new_post.html.j2', title='New Post', form=form)


@app.route('/admin/posts/edit/<int:id>', methods=['POST', 'GET'])
@login_required
def edit_post(id):
    post = Post.query.filter_by(id=id).first()
    if not current_user.is_admin and current_user != post.author:
        abort(403)

    form = PostForm()

    if post is None:
        abort(404)

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.post.data
        db.session.add(post)
        db.session.commit()

        flash('Post <a href="%s">"%s"</a> has been updated.' % (url_for('post',
                                                                slug=post.slug), post.title))
        return redirect((url_for('edit_post', id=post.id)))
    else:
        print('test')
        form.post.data = post.content
        form.title.data = post.title

        return render_template('admin/edit_post.html.j2', title='Edit Post', form=form)
