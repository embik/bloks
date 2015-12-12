from blog import app, db
from blog.forms import PostForm
from blog.models import Post
from blog.utils import create_slug
from flask import render_template, flash, url_for, redirect, abort
from flask.ext.login import login_required, current_user
from datetime import datetime


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
    form = PostForm()
    post = Post.query.filter_by(id=id).first()

    if post is None:
        abort(404)

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.post.data
        db.session.add(post)
        db.session.commit()

        flash('Post "%s" has been updated.' % post.title)
        return redirect((url_for('edit_post', id=post.id)))
    else:
        print('test')
        form.post.data = post.content
        form.title.data = post.title

        return render_template('admin/edit_post.html.j2', title='Edit Post',    form=form)
