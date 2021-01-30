from flask import Flask

from snakeeyes.blueprints.page import page
from snakeeyes.blueprints.contact import contact
from snakeeyes.extensions import debug_toolbar, mail, Csrf



""" If the settings_override is defined, the config will be updated to the settings_override parameter, if not, the config settings.py is used. """

def create_app(settings_override = None):


	app = Flask(__name__, instance_relative_config = True)

	"""Go to the folder config which is relative to the app.yp folder and check settings """
	app.config.from_object('config.settings')  
	"""Go to the instance folder and search for settings.py is it exist inside the config folder, if not, report silent i.e do not give error   """
	app.config.from_pyfile('settings.py', silent=True)

	# @app.route('/')
	# def index():
	# 	return app.config['HELLO']

	if settings_override:
		"""
			app.config.update() help to update settings.py file in the config file 
		"""
		app.config.update(settings_override)

	app.register_blueprint(page)
	app.register_blueprint(contact)
	extension(app)

	return app


def extension(app):
	"""

	Register 0 or more extensions (mutates the app passed in).

	:param app: Flask application instance 
	:return : None

	"""
	debug_toolbar.init_app(app)
	mail.init_app(app)
	Csrf.init_app(app)

	return None




