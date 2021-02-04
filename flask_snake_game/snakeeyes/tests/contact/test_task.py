from snakeeyes.extensions import mail


class TestTasks(object):	
	def test_deliver_support_email(self):
		form = {
			'email' : 'ola@gmai.cm',
			'message' : 'Hello skina '

		}

		with mail.record_messages() as outbox:
			deliver_contact_email(form.get('email'), form.get('message'))
			assert len(outbox) == 1
			assert form.get('email') in outbox[0].body