from snakeeyes.blueprints.user.models import User


class TestUserModel(object):
	"""docstring for TestUserModel"""
	def test_token_count(self, token):
		'''Function to verify that our token is working'''
		assert token.count('.') == 2
		
	def test_token_verify(self, token):
		user = User.deserializer_token(token)

		assert user.email == 'admin@local.host'

	def test_token_fail(self, token):
		user = User.deserializer_token('{0}123'.format(token))

		assert user is None 






