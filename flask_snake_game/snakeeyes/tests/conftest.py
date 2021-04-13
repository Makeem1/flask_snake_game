import pytest 

from snakeeyes.app import create_app
from snakeeyes.extensions import db as _db
from snakeeyes.blueprints.user.models import User

@pytest.yield_fixture(scope='session')
def app():
	'''
	Setting up flask test app, this only get executed at the 
	beginning of the session 

	:return : flask app 
	'''

	params = {
		'DEBUG' : False,
		'TESTING' : True
	}

	_app = create_app(settings_override=params)

	# Extablish application context before running the test
	ctx = _app.app_context()

	ctx.push()

	yield _app

	ctx.pop()


@pytest.yield_fixture(scope='function')
def client(app):
	'''
	Set up an app client, which is executed per test function
	'''

	yield app.test_client()


@pytest.yield_fixture(scope='session')
def db(app):
	"""
	Setup database, this only get executed once in a session
	:param: pytest fixture 
	:return : SQLAlchemy database session
	"""

	# Create a db table 
	_db.drop_all()
	_db.create_all()

	params = {
		'role' : 'admin',
		'email' : 'admin@local.host',
		'password' : 'devpassword'
	}

	admin = User(**params)

	_db.session.add(admin)
	_db.session.commit()

	return _db


@pytest.yield_fixture()
def session(db):
	"""
	Allow very fast tests by using rollback ands dnested session.
	:params: pytest fixtures
	:return : None
	"""

	db.session.begin_nested

	yield db.session

	db.session.rollback()


@pytest.fixture(scope='session')
def token(db):
	"""
	SErialize JWS token
	:param: pytest fixture
	:return : JWS token 
	"""

	user = User.find_by_identity('admin@local.host')

	return user.serialize_token()


@pytest.fixture(scope='function')
def users(db):
	"""
	Create a user fixtures. They reset per test 
	:param: pytest fixtures
	:return : SQLAlchemy database session
	"""

	db.session.query(User).delete()

	users = [
		{
			'role' : 'admin',
			'email' : 'admin@local.host',
			'password' : 'passsword'
		},

		{
			'active' : False,
			'email' : 'diable@local.com',
			'password' : 'password' 
		}
	]

	for user in users:
		db.session.add(User(**user))

	db.session.commit()

	return db 