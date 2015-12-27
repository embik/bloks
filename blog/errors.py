from blog.utils import render_theme_template
from blog import app


@app.errorhandler(401)
def unauthorized(e):
    return render_theme_template('errors/401.html.j2', title='Unauthorized'), 401


@app.errorhandler(403)
def access_forbidden(e):
    return render_theme_template('errors/403.html.j2', title='Forbidden'), 403


@app.errorhandler(404)
def page_not_found(e):
    return render_theme_template('errors/404.html.j2', title='Not Found'), 404


@app.errorhandler(500)
def server_error(e):
    return render_theme_template('errors/500.html.j2', title='Internal Server Error'), 500
