from flask import redirect, flash, url_for
from flask.ext.login import login_user
from werkzeug.security import generate_password_hash, check_password_hash
from blog.models import User, Hash


def try_login(username, password):
    user = User.query.filter_by(nickname=username).first()
    if user is not None:
        h = Hash.query.filter_by(user_id=user.id).first()
        if h is not None and check_password_hash(h.passwd_hash, password):
            login_user(user)
            flash('Successfuly signed in as %s' % user.nickname)
            return redirect(url_for('page'))

    flash('Login failed!')
    return redirect(url_for('login'))


def create_hash(password):
    return generate_password_hash(password)
