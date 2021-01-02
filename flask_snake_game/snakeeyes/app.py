from flask import Flask

from snakeeyes.blueprints.page import page

def create_app():


	app = Flask(__name__, instance_relative_config = True)

	app.config.from_object('config.settings')
	app.config.from_pyfile('settings.py', silent=True)

	# @app.route('/')
	# def index():
	# 	return app.config['HELLO']

	app.register_blueprint(page)

	return app

