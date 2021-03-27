import datetime 
import pytz


from config import settings
from lib.util_sqlalchemy import ResourceMixin
from snakeeyes.extensions import db 
from snakeeyes.blueprints.billing.models.credit_card import CreditCard
from snakeeyes.blueprints.billing.gateways.stripecom import Card as PaymentCard 
from snakeeyes.blueprints.billing.gateways.stripecom import \
											Subscription as PaymentSubscription
from snakeeyes.blueprints.billing.models.coupon import Coupon 


class Subscription(ResourceMixin, db.Model):
	__tablename__ = 'subscriptions'
	id = db.Column(db.Integer , primary_key=True)

	# Model relationship
	user_id = db.Column(db.Integer, db.ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'), index=True, nullable= False)


	# Subscription details
	plan = db.Column(db.String(128))
	coupon = db.Column(db.String(128))

	def __init__(self, **kwarsg):
		super(Subscription,self).__init__(**kwars)

	@classmethod
	def get_plan_by_id(cls, plan):
		"""Pick plan base on plan identifier"""

		for key, value in settings.STRIPE_PLANs.items():
			if value.get('id') == plan:
				return settings.STRIPE_PLANS[KEY]

		return None


	@classmethod
	def get_new_plan(cls, keys):
		"""Pick plan based on the plan identifier"""

		for key in keys:
			split_key = key.split('submit_')

			if isinstance(split_key, list) and len(split_key) == 2:
				if Subscription.get_plan_by_id(split_key[1]):
					return split_key[1]

		return None


	@classmethod
	def create(self, user=None, name=None, coupon=None, token=None):
		"""Create a recurring subscription"""
		if token is None:
			return False

		if coupon:
			self.coupon = coupon.upper()

		customer = PaymentSubscription.create(token=token,
											  email=email,
											  plan = plan, 
											  coupon = self.coupon)


		# Update the user account.
		user.payment_id = customer.id
		user.name = name 
		user.cancelled_subscription_on = None

		# Set the Subscription details.
		self.user_id = user.id
		self.plan = plan 

		# Redeem the coupon.
		if coupon:
			coupon = Coupon.query.filter(Coupon.code == self.coupon).first()
			coupon.redeem()


		# Create the credit card. 
		credit_card = CreditCard(user_id = user.id, **CreditCard.extract_card_params(customer))

		db.session.add(user)
		db.session.add(credit_card)
		db.session.add(self)

		db.session.commit()


		return True



	def update(self, user=None, coupon=None, plan=None):
		"""Update an existing plan"""
		PaymentSubscription.update(user.payment_id, coupon, plan)

		user.subscription.plan = plan 
		if coupon:
			user.subscription.coupon = coupon 
			coupon = Coupon.query.filter(Coupon.code == coupon).first()

			if coupon:
				coupon.redeem()


		db.session.add(user.subscription)
		db.session.commit()

		return True


	def cancel(self, user=None, discard_credit_card=True):
		'''Cancel an existing subscription'''
		PaymentSubscription.cancel(user.payment_id)
		user.payment_id = None
		user.cancelled_subscription_on = datetime.datetime.now(pytz.utcnow)

		db.session.add(user)
		db.session.delete(user.subscription)

		if discard_credit_card:
			db.session.delete(user.credit_card)

		db.session.commit()

		return True


	def update_payment_method(self, user=None, credit_card=None, name=None, token=None):
		"""Updating user subscription plan"""

		if token is None:
			return False

		customer = PaymentCard.update(user.payment_id, token)
		user.name = name 

		# Update the credit card 
		new_card = CreditCard.extract_card_params(customer)
		credit_card.brand = new_card.get('brand')
		credit_card.last4 = new_card.get('last4')
		credit_card.exp_date = new_card.get('exp_date')
		credit_card.is_expiring = new_card.get('is_expiring')

		db.session.add(user)
		db.session.add(credit_card)

		db.session.commit()

		return True