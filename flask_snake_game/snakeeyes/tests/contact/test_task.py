# from snakeeyes.extensions import mail
# from snakeeyes.blueprints.contact.tasks import deliver_contact_email


# class TestTasks(object):
#     def test_deliver_support_email(self):
#         """ Deliver a contact email. """
#         form = {
#           'email': 'foo@bar.com',
#           'message': 'Test message from Snake Eyes.'
#         }

#         with mail.record_messages() as outbox:
#             deliver_contact_email(form.get('email'), 
#                 form.get('message'))

#             # assert len(outbox) == 1
#             # assert outbox[0].subject == '[Snake Eyes] Contact'
#             # assert outbox[0].sender == form.get('email')
