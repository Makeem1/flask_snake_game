from flask import Flask

from snakeeyes.blueprints.page import page
from snakeeyes.extensions import debug_toolbar

def create_app(settings_override = None):


	app = Flask(__name__, instance_relative_config = True)

	app.config.from_object('config.settings')
	app.config.from_pyfile('settings.py', silent=True)

	# @app.route('/')
	# def index():
	# 	return app.config['HELLO']

	if settings_override:
		app.config.update(settings_override)

	app.register_blueprint(page)
	extension(app)

	return app


def extension(app):
	"""

	Register 0 or more extensions (mutates the app passed in).

	:param app: Flask application instance 
	:return : None

	"""
	debug_toolbar.init_app(app)

	return None




