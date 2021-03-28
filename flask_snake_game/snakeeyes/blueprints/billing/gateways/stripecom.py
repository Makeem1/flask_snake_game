import stripe 


class Card(object):
	@classmethod
	def update(cls, customer_id, stripe_token=None):
		"""Update an existing card through a customer"""

		customer = stripe.Customer.retrieve(customer_id)
		customer.source = stripe_token 

		return customer.save()


# This class is responsible for creating of plan in our application. 
class Plan(object):
	@classmethod
	def retrieve(cls, plan):
		"""Retrieve an existing plan ."""
		try:
			return stripe.Plan.retrieve(plan)
		except stripe.error.StripeError as e:
			print (e)

	@classmethod
	def list(cls):
		"""List all existing plan"""
		try:
			return stripe.Plan.all()
		except stripe.error.StripeError as e:
			print(e)

	@classmethod
	def create(cls, id = None, name = None, amount = None, 
		     currency = None, interval = None, interval_count = None, trial_period_days = None,
		     statement_descriptor = None, metadata = None):
		"""Create new subscriptions plan"""


		try:
			return stripe.Plan.create(id= id,
									  name = name,
									  amount = amount,
									  currency = currency,
									  interval = interval,
									  interval_count = interval_count,
									  trial_period_days = trial_period_days,
									  metadata = metadata, 
									  statement_descriptor = statement_descriptor
									  )

		except stripe.error.StripeError as e:
			print(e)


	@classmethod
	def update(cls, id = None, name = None, metadata = None, 
				statement_descriptor = None):
		"""Update exixting subscription plan """
		try:
			plan = stripe.Plan.retrieve(id)

			plan.name = name 
			plan.metadata = metadata
			plan.statement_descriptor = statement_descriptor
			return plan.save()
		except stripe.error.StripeError as e:
			print(e)


	@classmethod
	def delete(cls, plan):
		"""Delete an existing plan"""
		try:
			plan = stripe.Plan.retrieve(plan)
			return plan.delete()
		except stripe.error.StripeError as e:
			print(e)


class Subscription(object):
	@classmethod
	def create(cls, user=None, email=None, coupon=None, token=None):
		"""
			Create a new subscription.

        API Documentation:
          https://stripe.com/docs/api#create_subscription

        :param token: Token returned by JavaScript
        :type token: str
        :param email: E-mail address of the customer
        :type email: str
        :param coupon: Coupon code
        :type coupon: str
        :param plan: Plan identifier
        :type plan: str
        :return: Stripe customer
		"""

		params = {
			'source' : token,
			'email' : email ,
			'plan' : plan
 		}

		if coupon:
			params['coupon'] = 'coupon'


		return stripe.Customer.create(**params)


	@classmethod 
	def update(cls, customer_id=None, coupon=None, plan=None):
		"""Updating existing user plan"""

		customer = stripe.Customer.retrieve(customer_id)
		subscription_id = customer.subscriptions.data[0].id
		subscription = customer.subscriptions.retrieve(subscription_id)


		subscription.plan = plan 

		if coupon:
			subscription.coupon = coupon

		return subscription.save()

	@classmethod 
	def cancel(cls, customer_id=None):
		"""Cancel an existing subscritiop"""

		customer = stripe.Customer.retrieve(customer_id)
		subscription_id = customer.subscriptions.data[0].id

		return customer.subscriptions.retrieve(subscription_id)


class Coupon(object):
	@classmethod
	def create(cls, code=None, duration=None, amount_off = None,
				percent_off=None, currency=None, duration_in_months=None,
				max_redemptions=None, redeem_by=None):
		"""
		Create a new coupon code 

		"""

		return stripe.Coupon.create(id =code,
									duration=duration,
									amount_off=amount_off,
									percent_off=percent_off,
									currency=currency,
									duration_in_months=duration_in_months,
									max_redemptions=max_redemptions,
									redeem_by=redeem_by)


	@classmethod
	def delete(cls, id=None):
		"""
		Delete an existing coupon code
		"""
		coupon = stripe.Coupon.retrieve(id)
		return coupon.delete()


class Invoice(object):
	@classmethod
	def upcoming(cls, customer_id):
		"""
		Retreive an upcoming invoice item from a customer for a user. 

		:Param customer: stripe customer_id
		:param type : int
		:return : stripe invoice 
		"""

		return stripe.Invoice.upcoming(customer=customer_id)



class Event(object):
	@classmethod
	def retrieve(cls, event_id):
		"""
		Retrieve an event, this is used to validate the event in attempt to protect us 
		from potentially malicious events not sent from stripe.
		:param event_id: stripe event_id 
		:type: int
		:return : stripe event 
		"""

		return stripe.Event.retrieve(event_id)

		