import pytest 
from flask import url_for


def assert_status_with_message(status_code = 200, response = None, message=None):
	"""
    Check to see if a message is contained within a response.

    :param status_code: Status code that defaults to 200
    :type status_code: int
    :param response: Flask response
    :type response: str
    :param message: String to check for
    :type message: str
    :return: None
    """

	assert response.status_code == status_code
	assert message in str(response.data)


class ViewTestMixin:
    """Automatically loads in session and client for each test view"""

    @pytest.fixture(autouse = True)
    def set_common_fixture(self, session,client):
        self.session = session 
        self.client = client

    def login(self, identity='admin@local.host', password = 'password'):
        """Login a particualr user"""
        return login(self.client, identity, password)

    def logout(self):
        """Logout a particular user"""
        return (self.client)



def login(client, username='', password = ''):
    """This fucntion login in any user"""
    user = dict(
        identity = username,
        password = password
    )

    response = client.post(url_for('user.login'), data = user, follow_redirects=True)


def logout(client):
    """Logout any user"""
    return client.post(url_for('user.logout'), follow_redirects=True)