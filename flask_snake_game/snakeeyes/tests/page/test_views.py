from flask import url_for

class TestPage(object):
	def test_home_page(self, client):
		'''Hom page should respond with success'''
		response = client.get(url_for('page.home'))
		assert response.status_code == 200


	def test_terms_page(self, client):
		'''Terms page should respond with success '''
		response = client.get(url_for('page.terms'))
		assert response.status_code == 200


	def test_privacy_page(self, client):
		response = client.get(url_for('page.privacy'))
		assert response.status_code == 200


	def test_questions_page(self, client):
		response = client.get(url_for('page.questions'))
		assert response.status_code == 200

	def test_heads_page(self, client):
		response = client.get(url_for('page.questions'))
		assert '<title>FAQ-snake eyes application</title>' in str(response.data)
	

















	