import os
import re
from . import app, db
from .forms import PostForm, UserForm, CategoryForm, RemovalForm, LinkForm
from .models import Post, User, Category, Hash, Link
from .utils import create_slug, render_template, allowed_file
from .auth import create_hash, admin_required
from flask import flash, url_for, redirect, abort, request
from flask.ext.login import login_required, current_user
from werkzeug import secure_filename
from datetime import datetime
from sqlalchemy import desc


@app.route('/admin/dashboard')
@app.route('/admin/dashboard/page/<int:id>')
@login_required
def admin_dashboard(id=1):
    posts = Post.query.order_by(desc(Post.id)).\
        paginate(page=id, per_page=app.config['ADMIN_POSTS_PER_PAGE'])
    users = User.query.all()
    categories = Category.query.all()
    links = Link.query.all()
    return render_template('admin/dashboard.html.j2', posts=posts, users=users,
                           categories=categories, links=links, title='Dashboard',
                           no_description=True)


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
        # Do not allow privilege removal for the user's own account
        if current_user == user and user.is_admin is True and form.is_admin.data is False:
            flash('Updating user %s failed. You cannot remove administrative\
                   privileges from yourself!' % user.nickname, 'error')
            return redirect(url_for('admin_dashboard'))

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


@app.route('/admin/users/delete/<int:id>', methods=['POST', 'GET'])
@login_required
@admin_required
def delete_user(id):
    user = User.query.filter_by(id=id).first()
    if user is None:
        abort(404)
    if current_user == user:
        flash('Deleting user %s failed. You cannot remove your own user account!'
              % user.nickname, 'error')
        return redirect(url_for('admin_dashboard'))

    form = RemovalForm()
    if form.is_confirmed.data is True:
        Post.query.filter_by(user_id=id).delete()
        User.query.filter_by(id=id).delete()
        Hash.query.filter_by(user_id=id).delete()
        db.session.commit()

        flash('User %s has been deleted!' % user.nickname)
        return redirect(url_for('admin_dashboard'))
    else:
        msg = 'Warning: This will also remove all posts written by %s!' % user.nickname
        return render_template('admin/delete.html.j2', title='Delete User',
                               obj=user.nickname, form=form, msg=msg)


@app.route('/admin/categories/new', methods=['POST', 'GET'])
@login_required
@admin_required
def new_category():
    form = CategoryForm()
    if form.validate_on_submit():
        image = request.files['image']
        image_url = ''
        if image and allowed_file(image.filename):
            _, image_ext = os.path.splitext(secure_filename(image.filename))
            filename = 'category_%s%s' % (
                re.sub(r'[^a-z0-9_.-]', '_', form.name.data.lower()),
                image_ext
            )
            image_path = os.path.join(app.config['UPLOAD_DIR'], filename)
            image_url = os.path.join(app.config['UPLOAD_DIR_URL'], filename)
            image.save(image_path)
        category = Category(name=form.name.data, file_path=image_path, image_url=image_url)
        db.session.add(category)
        db.session.commit()

        flash('Category "%s" has been created!' % category.name)
        return redirect(url_for('admin_dashboard'))
    else:
        return render_template('admin/category.html.j2', title='New Category', form=form)


@app.route('/admin/categories/edit/<int:id>', methods=['POST', 'GET'])
@login_required
@admin_required
def edit_category(id):
    category = Category.query.filter_by(id=id).first()
    if category is None:
        abort(404)

    form = CategoryForm()
    if form.validate_on_submit():
        image = request.files['image']
        if category.name != form.name.data:
            category.name = form.name.data
            if not image:
                _, image_ext = os.path.splitext(category.file_path)
                filename = 'category_%s%s' % (
                    re.sub(r'[^a-z0-9_.-]', '_', form.name.data.lower()),
                    image_ext
                )
                image_path = os.path.join(app.config['UPLOAD_DIR'], filename)
                try:
                    os.rename(category.file_path, image_path)
                except OSError:
                    flash('Category image could not be moved!', 'warning')
                category.image_url = os.path.join(app.config['UPLOAD_DIR_URL'], filename)
                category.file_path = image_path

        if image and allowed_file(image.filename):
            _, image_ext = os.path.splitext(secure_filename(image.filename))
            filename = 'category_%s%s' % (
                re.sub(r'[^a-z0-9_.-]', '_', form.name.data.lower()),
                image_ext
            )
            image_path = os.path.join(app.config['UPLOAD_DIR'], filename)
            image_url = os.path.join(app.config['UPLOAD_DIR_URL'], filename)
            image.save(image_path)
            category.image_url = image_url
            category.file_path = image_path

        db.session.add(category)
        db.session.commit()

        flash('Category "%s" has been updated!' % category.name)
        return redirect(url_for('admin_dashboard'))
    else:
        form.name.data = category.name
        return render_template('admin/category.html.j2', title='Edit Category', form=form)


@app.route('/admin/categories/delete/<int:id>', methods=['POST', 'GET'])
@login_required
@admin_required
def delete_category(id):
    category = Category.query.filter_by(id=id).first()
    if category is None:
        abort(404)

    form = RemovalForm()
    if form.is_confirmed.data is True:
        posts = Post.query.filter_by(category_id=id).all()
        for post in posts:
            post.category_id = 0
            db.session.add(post)
        try:
            os.remove(Category.query.filter_by(id=id).first().file_path)
        except OSError:
            flash('Category image could not be deleted', 'warning')
        Category.query.filter_by(id=id).delete()
        db.session.commit()
        flash('Category %s has been deleted!' % category.name)
        return redirect(url_for('admin_dashboard'))
    else:
        msg = 'Warning: Posts will be marked as uncategorized'
        return render_template('admin/delete.html.j2', title='Delete Category',
                               obj=category.name, msg=msg, form=form)


@app.route('/admin/posts/new', methods=['POST', 'GET'])
@login_required
def new_post():
    form = PostForm()
    form.category.choices = [(0, 'Uncategorized')] + [(c.id, c.name)
                                                      for c in Category.query.all()]
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.post.data, timestamp=datetime.utcnow(),
                    slug=create_slug(form.title.data), user_id=current_user.id,
                    category_id=form.category.data)
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
    form.category.choices = [(0, 'Uncategorized')] + [(c.id, c.name)
                                                      for c in Category.query.all()]
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.post.data
        post.category_id = form.category.data
        db.session.add(post)
        db.session.commit()

        flash('Post <a href="%s">"%s"</a> has been updated.' % (url_for('post',
                                                                slug=post.slug), post.title))
        return redirect((url_for('edit_post', id=post.id)))
    else:
        form.post.data = post.content
        form.title.data = post.title
        form.category.data = post.category_id
        return render_template('admin/post.html.j2', title='Edit Post', form=form)


@app.route('/admin/posts/delete/<int:id>', methods=['POST', 'GET'])
@login_required
@admin_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()
    if post is None:
        abort(404)

    form = RemovalForm()
    if form.is_confirmed.data is True:
        Post.query.filter_by(id=id).delete()
        db.session.commit()

        flash('Post "%s" has been removed!' % post.title)
        return redirect(url_for('admin_dashboard'))
    else:
        return render_template('admin/delete.html.j2', title='Delete Post',
                               obj=post.title, form=form)


@app.route('/admin/links/new', methods=['POST', 'GET'])
@login_required
@admin_required
def new_link():
    form = LinkForm()
    if form.validate_on_submit():
        link = Link(label=form.label.data, url=form.url.data)
        db.session.add(link)
        db.session.commit()
        flash('Link "%s" has been created!' % link.label)
        return redirect(url_for('admin_dashboard'))
    else:
        return render_template('admin/link.html.j2', title='New Link', form=form)


@app.route('/admin/links/edit/<int:id>', methods=['POST', 'GET'])
@login_required
@admin_required
def edit_link(id):
    link = Link.query.filter_by(id=id).first()
    if link is None:
        abort(404)
    form = LinkForm()

    if form.validate_on_submit():
        link.label = form.label.data
        link.url = form.url.data
        db.session.add(link)
        db.session.commit()

        flash('Link "%s" has been updated!' % link.label)
        return redirect(url_for('admin_dashboard'))
    else:
        form.label.data = link.label
        form.url.data = link.url
        return render_template('admin/link.html.j2', title='Edit Link', form=form)


@app.route('/admin/links/delete/<int:id>', methods=['POST', 'GET'])
@login_required
@admin_required
def delete_link(id):
    link = Link.query.filter_by(id=id).first()
    if link is None:
        abort(404)

    form = RemovalForm()
    if form.is_confirmed.data is True:
        Link.query.filter_by(id=id).delete()
        db.session.commit()

        flash('Link "%s" has been removed!' % link.label)
        return redirect(url_for('admin_dashboard'))
    else:
        return render_template('admin/delete.html.j2', title='Delete Link',
                               obj=link.label, form=form)
