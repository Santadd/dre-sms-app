from flask import render_template
from app.errors import errors


#Create error responses
@errors.app_errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html', title='Error 404'), 404

@errors.app_errorhandler(403)
def forbidden(e):
    return render_template('errors/403.html', title='Error 403'), 403

@errors.app_errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html', title='Error 500'), 500

@errors.app_errorhandler(503)
def service_unavailable(e):
    return render_template('errors/503.html', title='Error 503'), 503
