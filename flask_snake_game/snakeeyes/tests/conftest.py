import pytest

from config import settings
from snakeeyes.app import create_app
from snakeeyes.extensions import db as _db
from snakeeyes.blueprints.user.models import User



@pytest.yield_fixture(scope='session')
def app():
	"""Seeting test application instance"""

	
	params = {
		'DEBUG' : False,
		'TESTING' : True,
		'WTF_CSRF_ENABLED': False,
		'SQLALCHEMY_DATABASE_URI': 'postgresql://clone:Olayinka1?@localhost:5430/clone'
	}

	_app = create_app(settings_override = params)

	ctx = _app.app_context()
	ctx.push()

	"""The code above the yield function serve as a set up i.e
		establishing a application context before running the test.
	"""
	yield _app
	"""The code below the yield function serve as a tear down i.e closing the 
		application context after running the test.
	"""
	ctx.pop()


@pytest.yield_fixture(scope='function')
def client(app):
	'''Setting up app client, this get executed for each test function in isolation. 
	  test_client() help us to make request to the url without starting the server.
	'''
	yield app.test_client()


@pytest.fixture(scope='session')
def db(app):
    """
    Setup our database, this only gets executed once per session.

    :param app: Pytest fixture
    :return: SQLAlchemy database session
    """
    _db.drop_all()
    _db.create_all()

    # Create a single user because a lot of tests do not mutate this user.
    # It will result in faster tests.
    params = {
        'role': 'admin',
        'email': 'admin@local.host',
        'password': 'password'
    }

    admin = User(**params)

    _db.session.add(admin)
    _db.session.commit()

    return _db


@pytest.yield_fixture(scope='function')
def session(db):
	"""
	Allow very fast test by using rollbacks and sessions.
	"""
	db.session.begin_nested()
	yield db.session
	db.session.rollback()


@pytest.fixture(scope='session')
def token(db):
	'''
	Serialize a JWS token
	'''
	user = User.find_by_identity('admin@local.host')
	return user.serialize_token()


@pytest.fixture(scope='function')
def users(db):
	"""create a user fixture. They reset per test."""
	db.session.query(User).delete()

	users = [
		{
			'role':'admin',
			'email':'disabled@local.host',
			'password':'password'
		},
		{
			'active':False,
			'email': 'disabled@local.host',
			'password': 'password'
		}
	]

	for user in users:
		db.session.add(User(**user))
	db.session.commit()

	return db


