from blog import app, db
from blog.forms import PostForm, UserForm, CategoryForm
from blog.models import Post, User, Category, Hash
from blog.utils import create_slug
from blog.auth import create_hash, admin_required
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
@admin_required
def new_user():
    form = UserForm()
    if form.validate_on_submit():
        user = User(nickname=form.nickname.data, is_admin=form.is_admin.data)
        db.session.add(user)
        db.session.commit()

        h = Hash(user_id=user.id, passwd_hash=create_hash(form.password.data))
        db.session.add(h)
        db.session.commit()

        flash('User %s has been created!' % user.nickname)
        return redirect(url_for('admin_dashboard'))
    else:
        return render_template('admin/user.html.j2', title='New User', form=form)


@app.route('/admin/users/edit/<int:id>', methods=['POST', 'GET'])
@login_required
@admin_required
def edit_user(id):
    user = User.query.filter_by(id=id).first()
    if user is None:
        abort(404)

    form = UserForm()
    if form.validate_on_submit():
        if len(form.password.data) > 0:
            h = Hash.query.filter_by(user_id=user.id).first()
            h.passwd_hash = create_hash(form.password.data)
            db.session.add(h)

        user.nickname = form.nickname.data
        user.is_admin = form.is_admin.data
        db.session.add(user)
        db.session.commit()

        flash('User %s has been updated!' % user.nickname)
        return redirect(url_for('admin_dashboard'))
    else:
        form.nickname.data = user.nickname
        form.is_admin.data = user.is_admin

        return render_template('admin/user.html.j2', title='Edit User', form=form)


@app.route('/admin/categories/new', methods=['POST', 'GET'])
@login_required
@admin_required
def new_category():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(name=form.name.data, image_url=form.image_url.data)
        db.session.add(category)
        db.session.commit()

        flash('Category "%s" has been created!' % category.name)
        return redirect(url_for('admin_dashboard'))
    else:
        return render_template('admin/category.html.j2', title='New Category',
                               form=form)


@app.route('/admin/categories/edit/<int:id>', methods=['POST', 'GET'])
@login_required
@admin_required
def edit_category(id):
    category = Category.query.filter_by(id=id).first()
    if category is None:
        abort(404)

    form = CategoryForm()
    if form.validate_on_submit():
        category.name = form.name.data
        category.image_url = form.image_url.data
        db.session.add(category)
        db.session.commit()

        flash('Category "%s" has been updated!' % category.name)
        return redirect(url_for('admin_dashboard'))
    else:
        form.name.data = category.name
        form.image_url.data = category.image_url
        return render_template('admin/category.html.j2', title='Edit Category',
                               form=form)


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
        return render_template('admin/post.html.j2', title='New Post', form=form)


@app.route('/admin/posts/edit/<int:id>', methods=['POST', 'GET'])
@login_required
def edit_post(id):
    post = Post.query.filter_by(id=id).first()
    if post is None:
        abort(404)
    if not current_user.is_admin and current_user != post.author:
        abort(403)

    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.post.data
        db.session.add(post)
        db.session.commit()

        flash('Post <a href="%s">"%s"</a> has been updated.' % (url_for('post',
                                                                slug=post.slug), post.title))
        return redirect((url_for('edit_post', id=post.id)))
    else:
        form.post.data = post.content
        form.title.data = post.title

        return render_template('admin/post.html.j2', title='Edit Post', form=form)
