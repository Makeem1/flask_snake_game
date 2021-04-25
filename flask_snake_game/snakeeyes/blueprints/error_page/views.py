from flask import Blueprint, render_template

error = Blueprint('error', __name__, template_folder='templates')

@error.app_errorhandler(404)
def page_not_found(e):
    return render_template('error/error_404.html'), 404

@error.app_errorhandler(500)
def server_error(e):
    return render_template('error/error_500.html'), 500


@error.app_errorhandler(429)
def page_limited(e):
	return render_template('error/error_429.html'), 429
	