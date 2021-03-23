import datetime 

from lib.util_sqlachemy import ResourceMixin 
from lib.util_datetime import timedelta_months 
from snakeeyes.extensions import db


class CreditCard(ResourceMixin, db.Model):
	IS_EXPIRING_THRESHOLD_MONTHS = 2

	__tablename__ = 'credit_cards'


	id = db.Column(db.Integer, primary_key=True)

	# Relationship with Users model
	user_id = db.Column(db.Integer, db.ForeignKey('users.id', onupdate='CASCADE'
						, ondelete='CASCADE'), index=True, nullable=False)

	# card details 
	brand = db.Column(db.String(32))
	last4 = db.column(db.Integer)
	exp_date = db.Column(db.Date, index=True)
	is_expiring = db.Column(db.Boolean(), nullable = False, server_default='0')

	def __init__(self, **kwargs):
		# call flask-sqlalchemy constructor
		super(CreditCard, self).__init__(**kwargs)

	@classmethod
	def is_expiring_soon(cls, compare_date=None, exp_date=None):
		"""To determine whether the card is expiring soon"""
		return exp_date <= timedelta_months(CreditCard.IS_EXPIRING_THRESHOLD_MONTHS, 
											compare_date=compare_date)


	@classmethod
	def mark_old_credit_cards(cls, compare_date=None):
		'''Mark cards that are going to expire soon''' 
		today_with_delta = timedelta_months(CreditCard.IS_EXPIRING_THRESHOLD_MONTHS, 
											compare_date)

		CreditCard.query.filter(CreditCard.exp_date <= today_with_delta).update({CreditCard.is_expiring=True})

		return db.session.commit()


	@classmethod
	def extract_card_params(cls, customer):
		"""Extract card info from paying customer"""

		card_data = customer.sources.data[0]
        exp_date = datetime.date(card_data.exp_year, card_data.exp_month, 1)

        card = {
            'brand': card_data.brand,
            'last4': card_data.last4,
            'exp_date': exp_date,
            'is_expiring': CreditCard.is_expiring_soon(exp_date=exp_date)
        }

        return card