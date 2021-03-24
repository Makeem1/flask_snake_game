from snakeeyes.app import create_celery_app
from snakeeyes.blueprints.user.models import User
from snakeeyes.blueprints.billing.models.credit_card import CreditCard



celery = create_celery_app()


@celery.task()
def mark_old_credit_cards():
	"""
	Mark credit cards that are going to expire soon. 
	"""

	return CreditCard.mark_old_credit_cards()