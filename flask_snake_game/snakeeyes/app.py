from flask import Flask
from celery import Celery 
from itsdangerous import URLSafeTimedSerializer


from snakeeyes.blueprints.page import page
from snakeeyes.blueprints.contact import contact
from snakeeyes.extensions import debug_toolbar, mail, Csrf, db , login 


CELERY_TASK_LIST = [ 'snakeeyes.blueprints.contact.tasks', ] 


def create_celery_app(app=None):
	"""Creating a celery app, accepting an app as argument and returning a celery instance"""
	app = app or create_app()

	celery = Celery(app.import_name, broker=app.config["CELERY_BROKER_URL"], 
					include=CELERY_TASK_LIST)
	celery.conf.update(app.config)

	TaskBase = celery.Task 

	class ContextTask(TaskBase):
		abstract = True

		def __call__(self, *args, **kwargs):
			with app.app_context():
				return TaskBase.__call__(self, *args, **kwargs)

	celery.Task = ContextTask
	return celery





login.login_view = 'user.login'
login.login_message = 'You need to login to access this page'
login.login_message_category = 'info'
login.session_protection = 'strong'


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
	db.init_app(app)
	login.init_app(app)

	return None
