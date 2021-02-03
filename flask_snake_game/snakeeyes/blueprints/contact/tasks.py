from snakeeyes.app import create_celery_app
from lib.flask_mailplus import send_template_message 

celery = create_celery_app()

@celery.task()
def deliver_contact_email(email, message):
	"""
		This function helps to assign task to a request by the user. The import send_template_message 
		takes all the parameter of the flask_mail extension
	"""


	ctx = {"email" : email, "message" : message}


	send_template_message(subject =' ["Snake Eyes"] Contact',
		sender=email,
		recipients=[celery.conf.get("MAIL_USERNAME")],
		reply_to=email, 
		template="contact/mail/index", ctx = ctx)