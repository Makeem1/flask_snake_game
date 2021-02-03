from flask import url_for 



class TestContact:
	def test_contact_page(self, client):
		response = client.get(url_for('contact.index'))
		assert response.status_code == 200 

	def test_contact_form:
		form = {
			"email" : 'makeem@gmail.com',
			"message" : "Testing contact form for snake application"
		}

		response = client.post(url_for('contact.index'), form = form , follow_redirects = True)

		assert response.status_code == 200
		assert 'Thanks' in str(response.data)
