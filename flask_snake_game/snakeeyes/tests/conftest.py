import pytest

from snakeeyes.app import create_app


@pytest.yield_fixture(scope='session')
def app():

	params = {
		'DEBUG' : False,
		'TESTING' : True,
	}

	_app = create_app(settings_override = params)

	ctx = _app.app_context()
	ctx.push()

	"""The code above the yield function serve as a set up """
	yield _app
	"""The code below the yield function serve as a tear down  """
	ctx.pop()


@pytest.yield_fixture(scope='function')
def client(app):
	'''Setting up app client, this get executed for each test function in isolation. test_client() help us to direct a test to a specific route '''
	yield app.test_client()